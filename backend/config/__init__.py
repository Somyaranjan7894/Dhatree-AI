"""
Dhatree AI Root Configuration Package.
Initializes Celery app so it is automatically discovered on Django startup.
"""
from __future__ import absolute_import, unicode_literals

# Ensure Celery app is loaded when Django starts
try:
    from .celery_app import app as celery_app

    __all__ = ("celery_app",)
except ImportError:
    pass
