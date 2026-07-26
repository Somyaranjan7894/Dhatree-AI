#!/usr/bin/env bash
# ==============================================================================
# Dhatree AI – Render Build Script
# Called by Render as the Build Command
# ==============================================================================
set -o errexit  # Exit on error

echo "=== Installing Python dependencies ==="
pip install --upgrade pip
pip install -r requirements/prod.txt

echo "=== Collecting static files ==="
python manage.py collectstatic --noinput

echo "=== Running database migrations ==="
python manage.py migrate --noinput

echo "=== Build complete ==="
