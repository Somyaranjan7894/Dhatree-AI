import os
import sys
import time

import django
from django.db import connections
from django.db.utils import OperationalError
from redis import Redis

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
django.setup()


def check_db():
    print("Checking Database connection...")
    try:
        conn = connections["default"]
        conn.cursor()
        print("[OK] Database connection successful.")
        return True
    except OperationalError as e:
        print(f"[FAIL] Database connection failed: {e}")
        return False


def check_redis():
    print("Checking Redis connection...")
    try:
        from django.conf import settings

        if getattr(settings, "CELERY_TASK_ALWAYS_EAGER", False):
            print("[OK] Celery is in EAGER mode. Skipping Redis connection check.")
            return True

        redis_url = getattr(settings, "CELERY_BROKER_URL", "redis://localhost:6379/1")
        r = Redis.from_url(redis_url)
        r.ping()
        print(f"[OK] Redis connection successful at {redis_url}.")
        return True
    except Exception as e:
        print(f"[FAIL] Redis connection failed: {e}")
        return False


def check_ai_registry():
    print("Checking AI Model Registry...")
    try:
        from ai_engine.models_registry.registry import ModelsRegistry

        registry = ModelsRegistry()
        models = registry._loaded_models
        print(f"[OK] AI Model Registry initialized. Models cached: {len(models)}")
        return True
    except Exception as e:
        print(f"[FAIL] AI Model Registry failed: {e}")
        return False


def check_gemini():
    print("Checking Gemini API Configuration...")
    try:
        from django.conf import settings

        api_key = getattr(settings, "GEMINI_API_KEY", None)
        model = getattr(settings, "GEMINI_MODEL", None)
        if api_key and model:
            print(f"[OK] Gemini config loaded. Model: {model}")
            return True
        else:
            print("[FAIL] Gemini config missing.")
            return False
    except Exception as e:
        print(f"[FAIL] Gemini config check failed: {e}")
        return False


if __name__ == "__main__":
    print("--- Backend Health Check ---")
    db_ok = check_db()
    redis_ok = check_redis()
    ai_ok = check_ai_registry()
    gemini_ok = check_gemini()

    if all([db_ok, redis_ok, ai_ok, gemini_ok]):
        print("\nAll health checks passed!")
        sys.exit(0)
    else:
        print("\nSome health checks failed.")
        sys.exit(1)
