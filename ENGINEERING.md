# Dhatree AI — Engineering Philosophy & Standards

This document sets the non-negotiable engineering principles and architectural rules for **Dhatree AI**. Every engineer, contributor, and AI coding assistant must strictly adhere to these standards across all phases of development.

---

## 1. Core Architectural Constraints

### A. Modular Monolith Architecture
Dhatree AI is built as a **Modular Monolith**. Every feature domain (`authentication`, `users`, `farms`, `crop_recommendation`, `disease_detection`, etc.) lives inside `backend/modules/` as an independent domain boundary.
- **Independence**: Modules must not directly inspect or mutate internal models of another module without going through clear service interfaces or public APIs.
- **High Cohesion & Low Coupling**: Code that changes together must stay together within a single module.

### B. Strict Layering Pattern
Every backend module must implement the four core layers:
1. **Views Layer (`views/`)**:
   - Only receives HTTP requests (`Request`), delegates payload validation to `Serializers`, invokes `Services`, and formats HTTP status codes (`Response`).
   - **CRITICAL**: Business logic must **NEVER** be placed inside Views.
2. **Services Layer (`services/`)**:
   - Encompasses all domain business rules, transaction management, and orchestration.
   - Inherits from `BaseService` (`backend/core/services/base.py`).
3. **Repositories Layer (`repositories/`)**:
   - Encapsulates all data access and ORM queries (`get_by_id`, `list_all`, `create`, `update`, `delete`, `soft_delete`).
   - Inherits from `BaseRepository` (`backend/core/repositories/base.py`).
   - Views and Services must never write raw `Model.objects.filter(...)` chains directly outside of repository methods.
4. **Data Layer (`models/`)**:
   - Django ORM models containing structural data attributes, UUID primary keys, verification flags, and audit timestamps (`created_at`, `updated_at`).

### C. Decoupled AI Layer (`ai_engine/`)
- All machine learning and computer vision execution must occur within `backend/ai_engine/`.
- **CRITICAL**: AI logic (`TensorFlow`, `PyTorch`, `OpenCV`, `Scikit-learn`) must **NEVER** exist inside Django API Views or standard domain serializers.
- Services interact with AI pipelines exclusively via abstract contracts (`PredictorInterface`, `AnalyzerInterface`) retrieved from the thread-safe `ModelsRegistry`.

---

## 2. API Design & Error Handling Standards

### Consistent JSON Response Schemas
All API endpoints must return standardized JSON structures regardless of success or failure.

#### Success Schema (`HTTP 200/201/204`)
```json
{
  "success": true,
  "message": "Operation completed successfully.",
  "data": { ... }
}
```

#### Error Schema (`HTTP 400/401/403/404/500`)
```json
{
  "success": false,
  "message": "Human readable summary of the error.",
  "errors": {
    "field_name": [ "Validation error detail message." ]
  }
}
```
- **Never expose internal exceptions or tracebacks to clients.** All unhandled exceptions must be caught by `core.exceptions.custom_exception_handler` and converted into the uniform error schema above.

---

## 3. Code Quality & Formatting Rules

1. **Keep Files Compact**: Never write monolithic files exceeding 500 lines. Split responsibilities logically into single-purpose components and utility modules.
2. **PEP8 Compliance**: All Python code must be formatted with `black` (`line-length = 88`) and ordered with `isort`.
3. **Type Safety**: Python functions must include type annotations (`typing` / `mypy` verified). TypeScript code (`frontend/src/`) must strictly avoid `any` and use Zod for runtime API payload verification.
4. **Environment Isolation**: Never hardcode secret keys, database URLs, or JWT secrets in source code. All secrets must be loaded via `python-dotenv` / `django-environ` from `.env`.
