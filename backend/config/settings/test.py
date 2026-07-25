"""
Testing Django settings for Dhatree AI Digital Agriculture Platform.
Uses fast password hashers and in-memory caching to maximize test speed.
"""
from .base import *

DEBUG = False

# Use fast password hashing in tests to speed up user creation fixtures
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Use fast local memory cache during tests instead of Redis
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Run Celery tasks synchronously in memory during tests
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Disable strict CORS/SSL in tests
SECURE_SSL_REDIRECT = False
CORS_ALLOW_ALL_ORIGINS = True
