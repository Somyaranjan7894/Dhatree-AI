# Dhatree AI Unified Code Quality Verification Script (PowerShell)
$ErrorActionPreference = "Stop"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "RUNNING DHATREE AI CODE QUALITY & LINTING SUITE" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Backend Python Checks
Write-Host "`n[+] Checking Backend (Python) Code Quality..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\..\backend"

if (Get-Command black -ErrorAction SilentlyContinue) {
    Write-Host "    -> Running Black formatting check..."
    black --check .
} else {
    Write-Host "    [Warning] Black not installed in active environment. Skipping." -ForegroundColor DarkYellow
}

if (Get-Command isort -ErrorAction SilentlyContinue) {
    Write-Host "    -> Running isort import ordering check..."
    isort --check-only .
} else {
    Write-Host "    [Warning] isort not installed in active environment. Skipping." -ForegroundColor DarkYellow
}

if (Get-Command flake8 -ErrorAction SilentlyContinue) {
    Write-Host "    -> Running Flake8 syntax and style validation..."
    flake8 .
} else {
    Write-Host "    [Warning] Flake8 not installed in active environment. Skipping." -ForegroundColor DarkYellow
}

Set-Location -Path "$PSScriptRoot\.."

# 2. Frontend Checks
Write-Host "`n[+] Checking Frontend (TypeScript + React) Code Quality..." -ForegroundColor Yellow
if (Test-Path "$PSScriptRoot\..\frontend\node_modules") {
    Set-Location -Path "$PSScriptRoot\..\frontend"
    Write-Host "    -> Running ESLint..."
    npm run lint
    Write-Host "    -> Running TypeScript static type verification..."
    npm run type-check
    Set-Location -Path "$PSScriptRoot\.."
} else {
    Write-Host "    [Warning] frontend/node_modules not found. Run 'npm install' inside frontend first." -ForegroundColor DarkYellow
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "ALL CODE QUALITY CHECKS COMPLETED!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
