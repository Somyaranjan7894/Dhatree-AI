# Installation Guide

## Local Development (Windows / macOS / Linux)

### 1. Database & Cache
Ensure PostgreSQL and Redis are installed. Alternatively, you can use Docker to run these dependencies:
\\\ash
cd docker
docker-compose up -d postgres redis
\\\

### 2. Backend Setup
\\\ash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate
pip install -r requirements/development.txt
cp ../.env.example ../.env  # Make sure to edit .env
python manage.py migrate
python manage.py runserver
\\\

### 3. Frontend Setup
\\\ash
cd frontend
npm install
npm run dev
\\\

## Using WSL2 on Windows
If using WSL2, follow the Linux instructions. Ensure your frontend and backend run on the same network interface, or use localhost routing provided by WSL.

