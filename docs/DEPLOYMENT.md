# Deployment Guide

Dhatree AI is designed to be deployed using a free-tier compatible stack.

## Architecture
- **Frontend**: Hosted on Vercel / Netlify.
- **Backend API**: Hosted on Render / Railway (Dockerized).
- **Database**: Neon (Serverless PostgreSQL).
- **Cache / Celery Broker**: Upstash (Serverless Redis).

## Required Environment Variables
Ensure the following variables are set on your backend hosting provider:
- \DJANGO_SETTINGS_MODULE=config.settings.production\
- \DJANGO_SECRET_KEY\ (Secure random string)
- \JWT_SECRET_KEY\
- \DATABASE_URL\
- \REDIS_URL\
- \CELERY_BROKER_URL\
- \GEMINI_API_KEY\
- \CORS_ALLOWED_ORIGINS\ (Set to your frontend URL)

For frontend hosting:
- \VITE_API_BASE_URL\ (Set to your backend URL)

