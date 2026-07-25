# Dhatree AI — Engineering Contribution Standards & Pull Request Guide

Thank you for contributing to Dhatree AI! To maintain a pristine, highly readable, and maintainable enterprise codebase, all contributors must adhere strictly to the engineering rules outlined in this document.

---

## 1. Code Style & Formatting Constraints

### A. Python (`backend/`)
- **Formatter**: `Black` (Strict line length: **88 characters**).
- **Import Ordering**: `isort` configured with `profile = "black"`.
- **Linter**: `Flake8` (`max-line-length = 88`, `extend-ignore = E203, W503`).
- **Type Annotations**: All function signatures must include exact parameter and return type hints (`typing` / `mypy` verified). Avoid `Any` wherever a concrete domain model or dictionary schema exists.
- **Docstrings**: Every class, method, and module must include clean descriptive docstrings explaining intent and return structures.

### B. TypeScript & React (`frontend/`)
- **Formatter & Linter**: `Prettier` + `ESLint`.
- **Type Safety**: **Zero implicit or explicit `any` allowed.** Every component prop must be defined using `interface` or `type`. All external API responses must be validated at runtime using `Zod` schemas (`src/modules/*/schemas/`).
- **Functional Components**: Use `React.FC` with explicit return JSX types (`JSX.Element`). Never use class components.

---

## 2. Git Branching & Commit Conventions

### Branch Naming
- `feature/<domain>-<short-description>` (e.g., `feature/auth-jwt-refresh`)
- `bugfix/<domain>-<short-description>` (e.g., `bugfix/crop-pipeline-nan`)
- `refactor/<domain>-<short-description>` (e.g., `refactor/core-base-repository`)

### Commit Messages
We follow Conventional Commits format:
```
<type>(<scope>): <short summary in present tense>

[optional detailed body explaining why the change was made]
```
Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`.
Example:
```
feat(auth): implement SimpleJWT token blacklisting upon logout

Enforces token rotation and blacklist verification inside custom LogoutService.
```

---

## 3. Pull Request Checklist

Before submitting a Pull Request, verify that:
1. You ran `./scripts/run_linters.sh` (or `.ps1`) and **all checks passed with zero warnings or errors**.
2. Your code adheres to the **Modular Monolith** boundaries (no business logic in Views or inside `core/`).
3. Your new API endpoints follow the consistent JSON response schema (`{"success": true, "message": "...", "data": {...}}`).
4. You added comprehensive automated unit tests (`pytest` for Python, `vitest` for TypeScript) verifying normal execution, edge cases, and failure modes.
5. You did not hardcode any sensitive credentials or environment keys.
