"""
Development Django settings for Dhatree AI Digital Agriculture Platform.
Enables debug mode, relaxed CORS, and verbose logging.
"""
from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Allow all CORS origins in development for easier React/Vite testing
CORS_ALLOW_ALL_ORIGINS = True

# Debug toolbar / verbose SQL logging if requested
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",  # Change to DEBUG to inspect all raw SQL
            "propagate": False,
        },
        "ai_engine": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
