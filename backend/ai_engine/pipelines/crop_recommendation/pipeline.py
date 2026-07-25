"""
Crop Recommendation AI Pipeline.
Implements `PredictorInterface` to analyze soil parameters (N, P, K, pH), weather metrics
(temperature, humidity, rainfall), and recommend optimal crop varieties.
"""

import logging
from typing import Any, Dict

import numpy as np

from ai_engine.interfaces.base import PredictorInterface
from ai_engine.models_registry import ModelsRegistry

logger = logging.getLogger(__name__)


def _load_joblib_model(registry_path):
    import joblib

    model_path = registry_path / "crop_recommendation" / "best_crop_model.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    logger.info(f"Loading real crop recommendation model from {model_path}")
    return joblib.load(model_path)


class CropRecommendationPipeline(PredictorInterface):
    """
    Predictive pipeline for crop variety recommendation.
    Now loads the trained artifact from registry to perform inference.
    """

    MODEL_KEY = "crop_recommendation_classifier"

    def __init__(self) -> None:
        self.registry = ModelsRegistry()
        self.model = None
        try:
            self.model = self.registry.get_model(self.MODEL_KEY, _load_joblib_model)
        except Exception as e:
            logger.warning(
                f"Crop model failed to load. Will fall back to mock. Error: {e}"
            )

    def load_model(self, model_path: str) -> None:
        """Load classification artifact (`RandomForest`/`XGBoost`) into model registry."""
        pass  # Handled by registry

    def preprocess(self, raw_features: Dict[str, Any]) -> np.ndarray:
        """
        Extract numerical soil and weather attributes:
        `['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']`
        """
        features = [
            float(raw_features.get("N", raw_features.get("nitrogen", 0.0))),
            float(raw_features.get("P", raw_features.get("phosphorus", 0.0))),
            float(raw_features.get("K", raw_features.get("potassium", 0.0))),
            float(raw_features.get("temperature", 0.0)),
            float(raw_features.get("humidity", 0.0)),
            float(raw_features.get("ph", 0.0)),
            float(raw_features.get("rainfall", 0.0)),
        ]
        return np.array([features], dtype=np.float32)

    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """
        Run model inference and return top recommended crop with confidence score.
        """
        if self.model is None:
            # Fallback mock
            return {
                "status": "success",
                "prediction": {
                    "recommended_crop": "rice",
                    "confidence_score": 0.0,
                    "alternatives": [],
                },
                "note": "Mock prediction used (model artifact missing).",
            }

        try:
            # The model is an sklearn pipeline and should have predict and predict_proba
            pred_crop = self.model.predict(features)[0]

            confidence = 0.0
            alternatives = []

            if hasattr(self.model, "predict_proba"):
                probas = self.model.predict_proba(features)[0]
                classes = self.model.classes_

                # Top 3 indices
                top_indices = np.argsort(probas)[::-1]
                confidence = float(probas[top_indices[0]])

                for idx in top_indices[1:4]:
                    alternatives.append(
                        {"crop": classes[idx], "confidence": float(probas[idx])}
                    )

            return {
                "status": "success",
                "prediction": {
                    "recommended_crop": pred_crop,
                    "confidence_score": confidence,
                    "alternatives": alternatives,
                },
                "note": "Real model inference.",
            }
        except Exception as e:
            logger.error(f"Error during crop prediction: {e}")
            return {"status": "error", "prediction": None, "error": str(e)}
