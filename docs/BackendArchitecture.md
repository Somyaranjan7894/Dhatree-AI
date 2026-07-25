# DHATREE AI - BACKEND ARCHITECTURE SPECIFICATION

Dhatree AI employs a strictly structured **Modular Monolith Architecture** with layered separation of concerns. This design guarantees production-grade reliability, testability, domain isolation, and seamless scalability as new agricultural intelligence capabilities (Farm Management, Crop Lifecycle, AI Engine, Weather, and Recommendation modules) are integrated.

---

## 1. Architectural Style: Modular Monolith

Unlike traditional Django applications that place fat models and fat views in tangled `apps`, Dhatree AI organizes domain boundaries into independent, self-contained **Modules** inside `backend/modules/`.

```
backend/
├── config/                  # Global settings, ASGI/WSGI, root URLs
├── core/                    # Shared horizontal infrastructure (responses, exceptions, RBAC, logging)
├── ai_engine/               # AI Engine bridges, pipeline wrappers, interfaces
└── modules/                 # Vertically sliced domain boundaries
    ├── users/               # Core identity, profiles, user management
    └── authentication/      # Authentication orchestration, JWT rotation, security
```

### Module Independence Rules
1. **No Cross-Module Database Queries**: Module `A` must NEVER directly import or query `models` from Module `B`.
2. **Inter-Module Communication via Services**: If `farm_management` needs to verify or fetch user details from `users`, it must call public methods exposed by `UserService` or `AuthService`.
3. **Encapsulated Scope**: Each module maintains its own models, repositories, domain services, serializers, views, URL configurations, and test suites.

---

## 2. Layered Separation of Concerns (The 4-Tier Pattern)

Every business domain module inside `backend/modules/` adheres strictly to a 4-tier separation of concerns:

```
+-------------------------------------------------------+
|  Tier 1: API / Transport Layer                        |
|  (views/*_views.py, serializers/*_serializers.py)     |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|  Tier 2: Domain Business Logic Layer                  |
|  (services/*_service.py)                              |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|  Tier 3: Data Persistence / Repository Layer          |
|  (repositories/*_repository.py)                       |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|  Tier 4: ORM & Database Schema Layer                  |
|  (models/*.py)                                        |
+-------------------------------------------------------+
```

### Tier 1: API / Transport Layer (`views/`, `serializers/`)
- **Responsibility**: HTTP protocol handling, request payload serialization/validation, OpenAPI (`drf-spectacular`) schema documentation, and delegation.
- **Constraints**:
  - **Zero Business Logic**: API views must NEVER perform calculations, workflow orchestration, or direct ORM queries (`User.objects.filter(...)`).
  - **Standardized Responses**: Views always return `success_response()` or `paginated_response()` defined in `core.responses`.

### Tier 2: Domain Business Logic Layer (`services/`)
- **Responsibility**: Encapsulates core agricultural rules, workflows, security checks, state transitions, and audit logging (`security_logger`, `app_logger`).
- **Constraints**:
  - **Protocol Agnostic**: Services accept pure Python primitives (`str`, `dict`, `UUID`) or Pydantic/dataclass models—never `HttpRequest` objects.
  - **Orchestrators**: Services invoke Repositories for data retrieval/persistence and dispatch background Celery tasks when asynchronous execution is required.

### Tier 3: Data Persistence Layer (`repositories/`)
- **Responsibility**: Isolates all database access, query optimization (`select_related`, `prefetch_related`, `only`), raw SQL abstractions, and custom filtering.
- **Constraints**:
  - **Encapsulated ORM**: No ORM calls bypass repositories.
  - **Soft Deletion Awareness**: Repositories automatically handle `is_deleted=False` invariants via custom model managers (`active_objects`).

### Tier 4: ORM & Database Schema Layer (`models/`)
- **Responsibility**: Defines PostgreSQL table schemas, indexes, constraints (`CheckConstraint`, `UniqueConstraint`), UUID primary keys, and data relationships.
- **Constraints**:
  - **No Complex Workflows**: Models only define schema properties and simple utility helpers (`check_password`, `soft_delete()`).

---

## 3. Shared Horizontal Infrastructure (`backend/core/`)

The `core/` package provides fundamental horizontal capabilities that every module consumes.

### Standardized JSON Response Schema (`core.responses`)
Every REST endpoint guarantees exact compliance with the Dhatree AI JSON contract:

**Success Response (`success_response`):**
```json
{
  "success": true,
  "message": "User account registered successfully.",
  "data": {
    "user": { "id": "uuid", "email": "..." },
    "tokens": { "access": "...", "refresh": "..." }
  }
}
```

**Paginated Success Response (`paginated_response`):**
```json
{
  "success": true,
  "message": "Users retrieved successfully.",
  "data": {
    "count": 142,
    "next": "https://api.dhatree.ai/api/v1/users/?page=2",
    "previous": null,
    "results": [ { ... }, { ... } ]
  }
}
```

### Global Custom Exception Handler (`core.exceptions`)
- Intercepts all validation failures, authentication errors, permission denials, and unexpected internal exceptions.
- Formats them into uniform error JSON payloads while logging full stack traces securely to `dhatree.error` without leaking server internals:
```json
{
  "success": false,
  "message": "Invalid input data.",
  "errors": {
    "email": ["An account with that email address already exists."]
  },
  "code": "validation_error"
}
```

### Role-Based Access Control (RBAC & `core.permissions`)
- `IsAuthenticated`: Ensures request contains valid access JWT.
- `IsAdmin`: Restricts endpoint execution to platform superusers or `admin` role profiles.
- `IsFarmer` / `IsAgronomist` / `IsResearcher`: Enforces strict agricultural role segregation.
- `OwnerOnly`: Guarantees multi-tenant isolation so farmers can only modify their own farms and crop cycles.
- `AdminOrReadOnly`: Allows public read access (`GET`) while restricting write mutations (`POST`, `PUT`, `DELETE`) to administrators.

---

## 4. Centralized Structured Logging

The platform utilizes three dedicated log streams configured via `dictConfig` in `config/settings/base.py`:
1. `dhatree.app`: Logs routine domain workflows, service executions, and background job transitions.
2. `dhatree.security`: Audits security-sensitive events (successful/failed logins, account lockouts, token blacklisting, role changes).
3. `dhatree.error`: Captures unhandled system faults, database disconnects, and AI inference failures with full diagnostic context.

---

## 5. Blueprint for Adding Future Modules

When implementing Phase 3+ modules (`farm_management`, `crop_lifecycle`, `disease_detection`, `weather`), developers must replicate the proven structure of `modules/users/`:

```
backend/modules/farm_management/
├── __init__.py
├── models/
│   ├── __init__.py
│   └── farm.py
├── repositories/
│   ├── __init__.py
│   └── farm_repository.py
├── services/
│   ├── __init__.py
│   └── farm_service.py
├── serializers/
│   ├── __init__.py
│   └── farm_serializers.py
├── views/
│   ├── __init__.py
│   └── farm_views.py
├── urls.py
└── tests/
    ├── __init__.py
    └── test_farms.py
```
This guarantees long-term maintainability, zero technical debt, and instant readiness for enterprise agriculture scaling.
