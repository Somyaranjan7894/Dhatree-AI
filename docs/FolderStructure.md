# Dhatree AI — Repository Folder Structure & Module Map

This document describes the comprehensive directory layout of Dhatree AI, mapping out every domain boundary and system layer.

```
dhatree_AI/
├── .github/
│   └── workflows/
│       ├── backend-ci.yml        # Python 3.13 Black, isort, Flake8, Pytest CI pipeline
│       └── frontend-ci.yml       # TypeScript type-check, ESLint, Vite build CI pipeline
├── .env.example                  # Environment variable template (Zero hardcoded secrets)
├── .gitignore                    # Python, Node, Docker, and AI/ML artifact exclusion rules
├── .pre-commit-config.yaml       # Git pre-commit hooks ensuring code formatting before commit
├── ENGINEERING.md                # Core engineering standards and SOLID constraints
├── README.md                     # Root project documentation entrypoint
│
├── docs/                         # Technical & Architectural Documentation
│   ├── Architecture.md           # Modular monolith architectural design & AI decoupling
│   ├── FolderStructure.md        # This repository map
│   ├── DevelopmentGuide.md       # Onboarding, environment setup, and Docker instructions
│   └── ContributionGuide.md      # Pull request standards and branch conventions
│
├── docker/                       # Multi-stage Containerization & Orchestration
│   └── docker-compose.yml        # Orchestration for Django (`8000`), Postgres, Redis, Vite (`5173`)
│
├── scripts/                      # Developer Automation & Quality Scripts
│   ├── setup_env.py              # Cross-platform environment verification & `.env` initializer
│   ├── run_linters.sh            # Shell runner for backend and frontend code verification
│   ├── run_linters.ps1           # PowerShell runner for Windows developer environments
│   └── scaffold_backend_modules.py # Automation tool for generating standard Django feature domains
│
├── backend/                      # Python 3.13 + Django 5 + DRF Backend Monolith
│   ├── Dockerfile                # Production multi-stage backend container build
│   ├── manage.py                 # Django command runner pointing to `config.settings.development`
│   ├── pyproject.toml            # Black, isort, and Pytest configuration specifications
│   ├── setup.cfg                 # Flake8 linting rules (`max-line-length = 88`)
│   │
│   ├── requirements/             # Segmented Dependency Management
│   │   ├── base.txt              # Production Core (Django, DRF, SimpleJWT, Celery, PyTorch, TF)
│   │   ├── dev.txt               # Developer tooling (pytest, black, isort, flake8)
│   │   ├── test.txt              # CI testing dependencies
│   │   └── prod.txt              # Production runtime drivers (`gunicorn`)
│   │
│   ├── config/                   # Root Project Configuration (`ROOT_URLCONF` & `WSGI/ASGI`)
│   │   ├── settings/
│   │   │   ├── base.py           # Shared settings across all runtimes
│   │   │   ├── development.py    # Local dev overrides (`DEBUG = True`, local SQLite fallback)
│   │   │   ├── production.py     # Production hardening (`ALLOWED_HOSTS`, HTTPS enforcement)
│   │   │   └── test.py           # Fast in-memory testing settings
│   │   ├── urls.py               # API Gateway router (`/api/v1/*`)
│   │   ├── wsgi.py               # WSGI entrypoint for synchronous production servers
│   │   └── asgi.py               # ASGI entrypoint for async / WebSocket scalability
│   │
│   ├── core/                     # Shared Foundation Layer (No Domain Business Logic)
│   │   ├── exceptions.py         # Standardized API error payload formatting (`custom_exception_handler`)
│   │   ├── pagination.py         # Standardized PageNumberPagination (`DhatreePageNumberPagination`)
│   │   ├── permissions.py        # Reusable RBAC Permission Classes (`IsAuthenticated`, `IsAdminUserOrReadOnly`)
│   │   ├── repositories/base.py  # Abstract `BaseRepository` with CRUD & soft delete ORM hooks
│   │   └── services/base.py      # Abstract `BaseService` ensuring consistent audit logging
│   │
│   ├── ai_engine/                # Decoupled Artificial Intelligence & Machine Learning Subsystem
│   │   ├── interfaces/base.py    # Abstract contracts: `PredictorInterface` and `AnalyzerInterface`
│   │   ├── models_registry/
│   │   │   ├── registry.py       # Thread-safe `ModelsRegistry` singleton for lazy loading
│   │   │   └── artifacts/        # Local model binary weights (`*.h5`, `*.pt`, `*.onnx`)
│   │   ├── pipelines/            # Domain-Specific AI Inference Execution Pipelines
│   │   │   ├── crop_recommendation/pipeline.py
│   │   │   ├── disease_detection/pipeline.py
│   │   │   └── fertilizer_recommendation/pipeline.py
│   │   └── utils/preprocessing.py # Image resizing and tabular normalization utilities
│   │
│   └── modules/                  # Independent Domain Feature Boundaries
│       ├── authentication/       # Phase 2: SimpleJWT authentication & token rotation
│       ├── users/                # Phase 2: Custom UUID `AbstractUser` and RBAC profiles
│       ├── farms/                # Phase 3: Farm boundary and geo-location management
│       ├── crop_recommendation/  # Phase 3: Soil/weather suitability analysis
│       ├── disease_detection/    # Phase 4: Computer vision screening portal
│       ├── disease_diagnosis/    # Phase 4: Detailed diagnostic and treatment recommendations
│       ├── soil_analysis/        # Soil test recording and NPK gap calculations
│       ├── fertilizer_recommendation/ # Precision nutrient dosing calculation
│       ├── weather_intelligence/ # Real-time micro-climate telemetry and alerts
│       ├── notifications/        # Multi-channel push/SMS/email alert dispatch
│       ├── dashboard/            # Aggregate farm metrics and platform telemetry
│       └── reports/              # PDF/Excel compliance and analytics report generation
│
└── frontend/                     # React 18 + TypeScript + Vite + Tailwind CSS Frontend
    ├── Dockerfile                # Production multi-stage Nginx container build
    ├── package.json              # React, TanStack Query, React Hook Form, Zod dependencies
    ├── tsconfig.json             # Strict static type checking rules
    ├── vite.config.ts            # Vite bundler configuration with `@/` path alias mapping
    ├── tailwind.config.ts        # Agricultural design system (`emerald`, `forest`, `amber`)
    ├── index.html                # Single page application entry HTML
    └── src/
        ├── main.tsx              # React DOM root renderer
        ├── App.tsx               # React Router layout navigation tree
        ├── api/                  # Centralized HTTP Networking Layer
        │   ├── client.ts         # Axios instance (`apiClient`) with JWT interceptors
        │   └── endpoints.ts      # Strictly typed API route endpoints
        ├── config/
        │   ├── constants.ts      # Global UI constants and status dictionaries
        │   └── env.ts            # Zod runtime environment variable validation (`import.meta.env`)
        ├── types/                # Shared TypeScript Type Definitions (`common.ts`, `api.ts`)
        ├── hooks/                # Reusable UI hooks (`useDebounce.ts`)
        ├── components/
        │   ├── common/           # UI Design System (`Button`, `Card`, `Input`, `Modal`, `Loader`)
        │   └── layout/           # App navigation (`Navbar`, `Sidebar`, `Layout`)
        ├── pages/                # Phase 1 Primary Route Visualizers (`Dashboard`, etc.)
        └── modules/              # Domain-Scoped Frontend Feature Modules
            ├── auth/             # Authentication forms and JWT management hooks
            ├── dashboard/        # Dashboard widgets and telemetry charts
            ├── farms/            # Farm creation and map visualization components
            ├── crop-recommendation/
            ├── disease-detection/
            └── fertilizer-recommendation/
```
