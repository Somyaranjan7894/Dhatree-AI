# DHATREE AI - AUTHENTICATION & SECURITY FLOW SPECIFICATION

Dhatree AI implements a secure, stateless authentication and authorization architecture built on **JSON Web Tokens (JWT)** via `djangorestframework-simplejwt` with mandatory refresh token rotation, token blacklisting, and Role-Based Access Control (RBAC).

---

## 1. JWT Configuration & Token Lifecycle

Tokens are generated and validated according to strict security lifecycles configured in `backend/config/settings/base.py`:
- **Access Token Lifetime**: 60 minutes (`timedelta(minutes=60)`).
- **Refresh Token Lifetime**: 7 days (`timedelta(days=7)`).
- **Token Rotation (`ROTATE_REFRESH_TOKENS: True`)**: Every time `/api/v1/auth/refresh/` is called with a valid refresh token, a new access token AND a new refresh token are issued.
- **Blacklisting (`BLACKLIST_AFTER_ROTATION: True`)**: The previous refresh token is immediately blacklisted in PostgreSQL (`token_blacklist` table) upon rotation or explicit logout. Any subsequent attempt to use a blacklisted token is rejected with `HTTP 401 Unauthorized`.

### Custom JWT Claims
Every issued access and refresh token embeds critical user identity attributes directly into its payload to prevent unnecessary database lookups on authenticated read endpoints:
```json
{
  "token_type": "access",
  "exp": 1721060000,
  "iat": 1721056400,
  "jti": "8f9a2b1c-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
  "user_id": "b5b590e2-3183-4070-8539-a7d45f7b27ea",
  "email": "farmer.ramesh@dhatree.ai",
  "username": "farmer_ramesh",
  "role": "farmer"
}
```

---

## 2. Authentication Sequence Diagrams

### 2.1 User Registration Flow (`POST /api/v1/auth/register/`)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Frontend Client
    participant API as RegisterAPIView
    participant Ser as RegisterSerializer
    participant Svc as AuthService
    participant Repo as UserRepository
    participant DB as PostgreSQL

    Client->>API: POST /api/v1/auth/register/ (email, username, password, role)
    API->>Ser: validate()
    Ser-->>API: validated_data
    API->>Svc: register(**validated_data)
    Svc->>Repo: check_email_exists() / check_username_exists()
    Repo->>DB: SELECT 1 WHERE email/username
    DB-->>Repo: Not Found
    Svc->>Repo: create_user_with_password()
    Repo->>DB: INSERT INTO users_user (hashed_password, UUID, active=True)
    DB-->>Repo: User Instance
    Svc->>Svc: _generate_tokens_for_user(user)
    Svc->>logger: log_operation("register_user") & security_logger.info()
    Svc-->>API: (user, tokens)
    API-->>Client: HTTP 201 Created { success: true, data: { user, tokens } }
```

### 2.2 User Login Flow (`POST /api/v1/auth/login/`)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Frontend Client
    participant API as LoginAPIView
    participant Svc as AuthService
    participant Repo as UserRepository
    participant DB as PostgreSQL

    Client->>API: POST /api/v1/auth/login/ (identifier, password)
    API->>Svc: login(identifier, password)
    Svc->>Repo: get_by_email_or_username(identifier)
    Repo->>DB: SELECT * FROM users_user WHERE (email OR username) AND is_deleted=False
    DB-->>Repo: User Instance
    Svc->>User: check_password(password)
    alt Invalid Password or Soft Deleted
        Svc->>security_logger: warning("Failed login attempt")
        Svc-->>API: raise AuthenticationFailed(HTTP 401)
    else Account Suspended
        Svc->>security_logger: warning("Login attempt on suspended account")
        Svc-->>API: raise PermissionDenied(HTTP 403)
    else Valid Credentials & Active Account
        Svc->>Svc: _generate_tokens_for_user(user)
        Svc->>security_logger: info("Successful user login")
        Svc-->>API: (user, tokens)
        API-->>Client: HTTP 200 OK { success: true, data: { user, tokens } }
    end
```

### 2.3 Token Rotation & Logout Blacklisting (`POST /api/v1/auth/refresh/` & `/logout/`)

```mermaid
sequenceDiagram
    autonumber
    actor Client as Frontend Client
    participant API as Refresh / Logout APIView
    participant Svc as AuthService
    participant BL as SimpleJWT Blacklist
    participant DB as PostgreSQL

    Note over Client,DB: Token Rotation (/api/v1/auth/refresh/)
    Client->>API: POST /api/v1/auth/refresh/ { "refresh": "old_refresh_token" }
    API->>Svc: refresh_tokens(old_refresh_token)
    Svc->>BL: RefreshToken(old_refresh_token)
    BL->>DB: Check token_blacklist table
    alt Token is already blacklisted or expired
        BL-->>Svc: raise TokenError
        Svc-->>API: raise AuthenticationFailed(HTTP 401)
    else Valid Refresh Token
        BL->>DB: INSERT old_refresh_token INTO token_blacklist (BLACKLIST_AFTER_ROTATION)
        BL->>Svc: Issue new_access & new_refresh tokens
        Svc-->>API: { "access": "new_access", "refresh": "new_refresh" }
        API-->>Client: HTTP 200 OK
    end

    Note over Client,DB: User Logout (/api/v1/auth/logout/)
    Client->>API: POST /api/v1/auth/logout/ { "refresh": "current_refresh_token" }
    API->>Svc: logout(current_refresh_token)
    Svc->>BL: RefreshToken.blacklist()
    BL->>DB: INSERT current_refresh_token INTO token_blacklist
    Svc->>security_logger: info("Refresh token successfully blacklisted upon logout.")
    API-->>Client: HTTP 200 OK { success: true, message: "Logged out and token blacklisted successfully." }
```

---

## 3. Account Lifecycle & Security Guards

Every authentication operation checks the user's account status (`account_status` and `is_deleted` flags):

| Account Status / Flag | Login (`/login/`) Behavior | API Request Behavior (`IsAuthenticated`) |
| :--- | :--- | :--- |
| `is_active: True`, `account_status: 'active'` | **200 OK** + JWT Tokens Issued | **200 OK** (Allows API access based on RBAC) |
| `account_status: 'suspended'` | **403 Forbidden** (`PermissionDenied`) | **403 Forbidden** (Custom JWT middleware / verification checks) |
| `is_deleted: True` (Soft Deleted) | **401 Unauthorized** (Account not found in active pool) | **401 Unauthorized** |
| `is_active: False` | **401 Unauthorized** (`AuthenticationFailed`) | **401 Unauthorized** |

---

## 4. Role-Based Access Control (RBAC) Matrix

Dhatree AI enforces strict permission boundaries across roles (`User.Role`):

| Role | Permitted Actions | Restricted Actions |
| :--- | :--- | :--- |
| `admin` (`IsAdmin`) | List all users (`GET /api/v1/users/`), soft-delete any account (`DELETE /api/v1/users/{id}/`), global read/write across all modules. | Cannot hard-delete audit logs or bypass database constraints. |
| `farmer` (`IsFarmer`) | Register, update own profile (`PUT /api/v1/auth/profile/`), manage own farms, crops, and disease scans (`OwnerOnly`). | **403 Forbidden** when attempting to list users or access other farmers' farms. |
| `agronomist` (`IsAgronomist`) | Review disease scans assigned to their territory, publish advisory notes, manage recommendation rules. | **403 Forbidden** when attempting administrative user deletions. |
| `researcher` (`IsResearcher`) | Read-only access (`AdminOrReadOnly`) to anonymized disease scan aggregations and model inference logs. | **403 Forbidden** on farmer profile modifications or farm mutations. |
