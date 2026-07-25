# DHATREE AI - REST API DOCUMENTATION & SCHEMA CONTRACT

Dhatree AI exposes a clean, versioned RESTful API (`/api/v1/`) fully documented using **OpenAPI 3.0** via `drf-spectacular`.

---

## 1. OpenAPI & Interactive Documentation Endpoints

When running the platform locally (`python manage.py runserver` or Docker Compose), interactive API schemas are available without manual authentication setup:

- **Interactive Swagger UI**: `http://localhost:8000/api/v1/docs/swagger/`
- **ReDoc UI**: `http://localhost:8000/api/v1/docs/redoc/`
- **Raw OpenAPI 3.0 JSON Schema**: `http://localhost:8000/api/v1/schema/`

---

## 2. Standardized Response & Error Contracts

To simplify frontend application state management and API error handling, **every** REST endpoint in Dhatree AI returns JSON payloads conforming strictly to the following envelopes:

### 2.1 Standard Success Envelope (`200 OK`, `201 Created`)
```json
{
  "success": true,
  "message": "Human-readable confirmation summary.",
  "data": {
    ... endpoint specific domain object or key-value dictionary ...
  }
}
```

### 2.2 Standard Paginated Success Envelope (`200 OK`)
```json
{
  "success": true,
  "message": "Users retrieved successfully.",
  "data": {
    "count": 142,
    "next": "http://localhost:8000/api/v1/users/?page=2",
    "previous": null,
    "results": [
      {
        "id": "72557e9d-ef66-47a5-bdf2-dfcb47783271",
        "email": "farmer.gopal@dhatree.ai",
        "username": "farmer_gopal",
        "full_name": "Gopal Rao",
        "role": "farmer",
        "account_status": "active",
        "is_verified": true,
        "created_at": "2026-07-15T12:00:00Z"
      }
    ]
  }
}
```

### 2.3 Standard Error Envelope (`400`, `401`, `403`, `404`, `500`, `503`)
```json
{
  "success": false,
  "message": "Invalid input data.",
  "errors": {
    "email": ["An account with that email address already exists."],
    "password": ["This password is too short. It must contain at least 10 characters."]
  },
  "code": "validation_error"
}
```

### Error Code Reference (`code` field)
| Code | HTTP Status | Description |
| :--- | :--- | :--- |
| `validation_error` | `400 Bad Request` | Request body or query parameters failed schema/business validation. |
| `business_rule_violation` | `400 Bad Request` | Domain constraint violated (e.g., trying to start a crop cycle on an inactive farm). |
| `authentication_failed` | `401 Unauthorized` | Missing, expired, malformed, or blacklisted JWT access/refresh token. |
| `permission_denied` | `403 Forbidden` | Authenticated user lacks required role (`IsAdmin`, `IsFarmer`) or resource ownership. |
| `resource_not_found` | `404 Not Found` | Requested UUID does not exist or has been soft-deleted (`is_deleted=True`). |
| `ai_inference_error` | `503 Service Unavailable` | AI Engine model prediction or computer vision pipeline is temporarily unavailable. |
| `internal_error` | `500 Internal Server Error` | Unexpected system fault. Traceback is logged securely to `dhatree.error`. |

---

## 3. Authentication & Account Lifecycle Endpoints (`/api/v1/auth/`)

### `POST /api/v1/auth/register/`
Registers a new platform user account and issues initial access/refresh JWT tokens.
- **Permission**: Public (`AllowAny`)
- **Request Body**:
  ```json
  {
    "email": "farmer.ramesh@dhatree.ai",
    "username": "farmer_ramesh",
    "password": "StrongPassword123!",
    "password_confirm": "StrongPassword123!",
    "full_name": "Ramesh Kumar",
    "phone_number": "+919876543210",
    "role": "farmer"
  }
  ```
- **Response (`201 Created`)**:
  ```json
  {
    "success": true,
    "message": "User account registered successfully.",
    "data": {
      "user": {
        "id": "c47549b8-4adf-4f14-8422-18c2fa543ad3",
        "email": "farmer.ramesh@dhatree.ai",
        "username": "farmer_ramesh",
        "full_name": "Ramesh Kumar",
        "role": "farmer"
      },
      "tokens": {
        "access": "eyJhbGciOiJIUzI1NiIsIn...",
        "refresh": "eyJhbGciOiJIUzI1NiIsIn..."
      }
    }
  }
  ```

---

### `POST /api/v1/auth/login/`
Authenticates a user via `email` or `username` along with their password.
- **Permission**: Public (`AllowAny`)
- **Request Body**:
  ```json
  {
    "identifier": "farmer.ramesh@dhatree.ai",
    "password": "StrongPassword123!"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Logged in successfully.",
    "data": {
      "user": { ... },
      "tokens": {
        "access": "eyJhbGciOiJIUzI1NiIsIn...",
        "refresh": "eyJhbGciOiJIUzI1NiIsIn..."
      }
    }
  }
  ```

---

### `POST /api/v1/auth/refresh/`
Rotates the JWT token pair. Requires a valid, unexpired, and non-blacklisted refresh token.
- **Permission**: Public (`AllowAny`)
- **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsIn..."
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Token refreshed successfully.",
    "data": {
      "access": "eyJhbGciOiJIUzI1NiIsIn_new_access...",
      "refresh": "eyJhbGciOiJIUzI1NiIsIn_new_refresh..."
    }
  }
  ```

---

### `POST /api/v1/auth/logout/`
Logs out the user by permanently adding the supplied refresh token to the PostgreSQL `token_blacklist` table.
- **Permission**: Public (`AllowAny`)
- **Request Body**:
  ```json
  {
    "refresh": "eyJhbGciOiJIUzI1NiIsIn..."
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Logged out and token blacklisted successfully.",
    "data": {}
  }
  ```

---

### `GET /api/v1/auth/me/`
Retrieves the full profile details of the currently authenticated user.
- **Permission**: Authenticated (`IsAuthenticated` - requires `Authorization: Bearer <access_token>`)
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Profile retrieved successfully.",
    "data": {
      "id": "c47549b8-4adf-4f14-8422-18c2fa543ad3",
      "email": "farmer.ramesh@dhatree.ai",
      "username": "farmer_ramesh",
      "full_name": "Ramesh Kumar",
      "phone_number": "+919876543210",
      "role": "farmer",
      "account_status": "active",
      "is_verified": false
    }
  }
  ```

---

### `PUT / PATCH /api/v1/auth/profile/`
Updates the authenticated user's profile attributes. Attempts to tamper with privileged fields (`role`, `is_verified`, `is_active`) are silently stripped or rejected.
- **Permission**: Authenticated (`IsAuthenticated`)
- **Request Body (`PATCH`)**:
  ```json
  {
    "full_name": "Ramesh Kumar Updated",
    "phone_number": "+918888888888"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Profile updated successfully.",
    "data": {
      "id": "c47549b8-4adf-4f14-8422-18c2fa543ad3",
      "full_name": "Ramesh Kumar Updated",
      "phone_number": "+918888888888"
    }
  }
  ```

---

### `POST /api/v1/auth/change-password/`
Changes the authenticated user's password after verifying their existing password.
- **Permission**: Authenticated (`IsAuthenticated`)
- **Request Body**:
  ```json
  {
    "old_password": "StrongPassword123!",
    "new_password": "NewStrongPassword456!",
    "new_password_confirm": "NewStrongPassword456!"
  }
  ```
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Password changed successfully.",
    "data": {}
  }
  ```

---

## 4. User Management Endpoints (`/api/v1/users/`)

### `GET /api/v1/users/`
Returns a paginated list of active platform users. Supports filtering, searching, and sorting.
- **Permission**: Administrator Only (`IsAdmin`)
- **Query Parameters**:
  - `role`: Filter by role (`farmer`, `agronomist`, `researcher`, `admin`).
  - `account_status`: Filter by status (`active`, `suspended`, `pending_verification`).
  - `search`: Full-text search across `email`, `username`, and `full_name`.
  - `ordering`: Sort by field (e.g., `-created_at`, `username`).
  - `page`: Page number (`?page=2`).
- **Response (`200 OK`)**: Standard Paginated Success Envelope.

---

### `GET /api/v1/users/{uuid}/`
Retrieves a specific user profile by their UUID.
- **Permission**: Authenticated (`IsAuthenticated`)
- **Response (`200 OK`)**: Standard Success Envelope.

---

### `PATCH /api/v1/users/{uuid}/`
Partially updates a target user's profile details.
- **Permission**: Authenticated (`IsAuthenticated` - users can update their own profile; admins can update any profile).
- **Response (`200 OK`)**: Standard Success Envelope.

---

### `DELETE /api/v1/users/{uuid}/`
Deactivates (`soft-deletes`) a user account. Sets `is_deleted = True`, `is_active = False`, and records timestamp in `deleted_at`.
- **Permission**: Administrator Only (`IsAdmin`)
- **Response (`200 OK`)**:
  ```json
  {
    "success": true,
    "message": "Account deactivated successfully.",
    "data": {}
  }
  ```
