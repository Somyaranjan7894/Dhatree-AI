# Dhatree AI Architecture

Dhatree AI follows a **Modular Monolith** pattern in Django. This approach combines the simplicity of a monolithic deployment with the strict domain boundaries of microservices.

## High-Level Flow
`React SPA` -> `Vite Dev Server / Nginx` -> `Django REST Framework` -> `Domain Services` -> `PostgreSQL / Redis / AI Engine`

## Directory Structure
- `backend/core`: Shared utilities, custom exceptions, global pagination, and base models.
- `backend/modules`: Independent domain modules.
  - `authentication`: JWT logic.
  - `farms` & `crops`: Farm management.
  - `ai_assistant`: Gemini integration.
  - `disease_detection`: Vision inference.
- `backend/ai_engine`: Pure Python ML pipelines, decoupled from Django models, making it easy to test and version independently.

## Data Layer
- **PostgreSQL**: Primary transactional store.
- **Redis**: Caching and Celery broker.
