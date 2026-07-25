# Dhatree AI — Local Development & Setup Guide

This guide walks you through setting up your local environment for Dhatree AI across both standalone Python/Node workflows and multi-container Docker orchestration.

---

## Prerequisites

Ensure your system has the following installed:
- **Python 3.10+** (Recommended: **3.13+**)
- **Node.js 18+** & **npm 9+**
- **Docker** & **Docker Compose** (v2+)
- **Git**

---

## 1. Automated Environment Initialization

Run our automated Python setup script to verify your system dependencies and generate your `.env` configuration file from the template:

```bash
python scripts/setup_env.py
```

Check the generated `.env` file at the root directory and ensure database URLs and JWT secrets match your preferred local settings.

---

## 2. Option A: Full Stack Docker Orchestration (Recommended for Quick Start)

Our multi-stage Docker setup spins up the complete platform (`Django API`, `PostgreSQL`, `Redis`, and `Vite Frontend`) with hot-reloading:

```bash
# Start all services in detached or interactive mode
docker compose up --build
```

### Accessing Local Services
- **Frontend Hub**: [http://localhost:5173](http://localhost:5173)
- **Backend API Gateway**: [http://localhost:8000/api/v1/](http://localhost:8000/api/v1/)
- **Interactive Swagger API Docs**: [http://localhost:8000/api/v1/docs/swagger/](http://localhost:8000/api/v1/docs/swagger/)
- **Interactive ReDoc API Docs**: [http://localhost:8000/api/v1/docs/redoc/](http://localhost:8000/api/v1/docs/redoc/)
- **PostgreSQL Database**: Port `5432` (User: `postgres`, DB: `dhatree_db`)
- **Redis Cache/Broker**: Port `6379`

---

## 3. Option B: Standalone Local Development (Recommended for Active Coding)

### A. Backend Setup (`backend/`)
```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux / macOS:
source venv/bin/activate
# On Windows (PowerShell):
.\venv\Scripts\Activate.ps1

# Install developer dependencies
pip install -r requirements/dev.txt

# Run migrations (defaults to local SQLite if DATABASE_URL not set)
python manage.py migrate

# Start Django development server
python manage.py runserver 8000
```

### B. Frontend Setup (`frontend/`)
Open a separate terminal instance:
```bash
cd frontend

# Install Node dependencies
npm install

# Start Vite development server with instant hot module replacement (HMR)
npm run dev
```

---

## 4. Running Automated Tests & Code Quality Verification

To verify code formatting (`Black`, `isort`, `Flake8`) and frontend type safety (`tsc`, `ESLint`) before pushing changes:

```bash
# On Linux / macOS:
./scripts/run_linters.sh

# On Windows (PowerShell):
powershell scripts/run_linters.ps1
```

To execute backend unit and integration tests across all modules (`users`, `authentication`):
```bash
cd backend
python manage.py test modules
# Or run with Pytest:
pytest
```
