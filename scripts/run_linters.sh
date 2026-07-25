#!/usr/bin/env bash
# Dhatree AI Unified Code Quality Verification Script
set -e

echo "=========================================================="
echo "RUNNING DHATREE AI CODE QUALITY & LINTING SUITE"
echo "=========================================================="

# 1. Backend Linting & Formatting Check
echo ""
echo "[+] Checking Backend (Python) Code Quality..."
cd backend

if command -v black >/dev/null 2>&1; then
    echo "    -> Running Black formatting check..."
    black --check .
else
    echo "    [Warning] Black not installed in active environment. Skipping."
fi

if command -v isort >/dev/null 2>&1; then
    echo "    -> Running isort import ordering check..."
    isort --check-only .
else
    echo "    [Warning] isort not installed in active environment. Skipping."
fi

if command -v flake8 >/dev/null 2>&1; then
    echo "    -> Running Flake8 syntax and style validation..."
    flake8 .
else
    echo "    [Warning] Flake8 not installed in active environment. Skipping."
fi

cd ..

# 2. Frontend Linting & Type Checking
echo ""
echo "[+] Checking Frontend (TypeScript + React) Code Quality..."
if [ -d "frontend/node_modules" ]; then
    cd frontend
    echo "    -> Running ESLint..."
    npm run lint
    echo "    -> Running TypeScript static type verification (`tsc`)..."
    npm run type-check
    cd ..
else
    echo "    [Warning] `frontend/node_modules` not found. Run `npm install` inside frontend/ first."
fi

echo ""
echo "=========================================================="
echo "ALL CODE QUALITY CHECKS PASSED SUCCESSFULLY!"
echo "=========================================================="
