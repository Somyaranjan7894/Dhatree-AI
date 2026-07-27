"""
Thread-safe Model Registry (`ModelsRegistry`).
Provides lazy-loading, caching, and version verification for ML/AI artifacts (`PyTorch`, `TensorFlow`, `Scikit-learn`)
so Django server startup remains instant while keeping inference memory efficient.
"""

import logging
import os
import threading
from pathlib import Path
from typing import Any, Dict, Optional

from core.exceptions import ModelInferenceError

logger = logging.getLogger(__name__)


class ModelsRegistry:
    """
    Singleton registry managing lifecycle of AI model artifacts in memory.
    """

    _instance: Optional["ModelsRegistry"] = None
    _lock = threading.Lock()

    def __new__(cls) -> "ModelsRegistry":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._loaded_models = {}
                from django.conf import settings

                cls._instance._registry_path = Path(settings.AI_MODEL_REGISTRY_PATH)
        return cls._instance

    def get_model(self, model_key: str, loader_callable: Any) -> Any:
        """
        Retrieve a model from memory cache or load via `loader_callable` if not cached.
        Thread-safe to prevent race conditions during high-concurrency requests.
        """
        if model_key in self._loaded_models:
            return self._loaded_models[model_key]

        with self._lock:
            # Double-check locking pattern
            if model_key in self._loaded_models:
                return self._loaded_models[model_key]

            logger.info(f"Loading AI model artifact into memory: [{model_key}]")
            logger.info(f"Resolved AI_MODEL_REGISTRY_PATH: {self._registry_path.resolve()}")
            try:
                model_artifact = loader_callable(self._registry_path)
                self._loaded_models[model_key] = model_artifact
                return model_artifact
            except Exception as exc:
                import traceback
                error_trace = traceback.format_exc()
                logger.error(f"Failed to load AI model [{model_key}]: {exc}\n{error_trace}")
                raise ModelInferenceError(
                    f"Model [{model_key}] could not be loaded: {exc}"
                )

    def unload_model(self, model_key: str) -> None:
        """Unload a specific model from memory cache to free RAM/VRAM."""
        with self._lock:
            if model_key in self._loaded_models:
                del self._loaded_models[model_key]
                import gc
                gc.collect()
                logger.info(f"Unloaded AI model from cache: [{model_key}]")
