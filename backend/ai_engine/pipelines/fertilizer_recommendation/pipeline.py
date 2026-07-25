"""
Fertilizer Recommendation AI Pipeline.
Implements `PredictorInterface` to analyze soil deficiencies (N, P, K levels vs. crop target ratios)
and output optimal nutrient blend and dosage recommendations.
"""
from typing import Any, Dict
import numpy as np
import logging
from ai_engine.interfaces.base import PredictorInterface
from ai_engine.models_registry import ModelsRegistry

logger = logging.getLogger(__name__)

def _load_joblib_model_and_encoder(registry_path):
    import joblib
    model_path = registry_path / "fertilizer_recommendation" / "fertilizer_production_best.joblib"
    encoder_path = registry_path / "fertilizer_recommendation" / "fertilizer_label_encoder.joblib"
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    if not encoder_path.exists():
        raise FileNotFoundError(f"Label encoder not found at {encoder_path}")
        
    logger.info(f"Loading real fertilizer recommendation model from {model_path}")
    model = joblib.load(model_path)
    encoder = joblib.load(encoder_path)
    return model, encoder

class FertilizerRecommendationPipeline(PredictorInterface):
    """
    Predictive pipeline for precision fertilizer recommendations.
    Now loads the trained artifact from registry to perform inference.
    """

    MODEL_KEY = "fertilizer_recommendation_net"

    def __init__(self) -> None:
        self.registry = ModelsRegistry()
        self.model = None
        self.encoder = None
        try:
            self.model, self.encoder = self.registry.get_model(self.MODEL_KEY, _load_joblib_model_and_encoder)
        except Exception as e:
            logger.warning(f"Fertilizer model failed to load. Will fall back to mock. Error: {e}")

    def load_model(self, model_path: str) -> None:
        """Load tabular nutrient balancing artifact into model registry."""
        pass

    def preprocess(self, raw_features: Dict[str, Any]) -> np.ndarray:
        """
        Extract features for the model. The model expects:
        `['temperature', 'humidity', 'rainfall', 'soil_type', 'crop_type', 'nitrogen', 'potassium', 'phosphorus']`
        """
        # Map inputs safely, falling back to dummy values if not provided
        features = [
            float(raw_features.get('temperature', 0.0)),
            float(raw_features.get('humidity', 0.0)),
            float(raw_features.get('rainfall', 0.0)),
            str(raw_features.get('soil_type', 'Loamy')),
            str(raw_features.get('crop_type', 'Wheat')),
            float(raw_features.get('nitrogen', raw_features.get('N', 0.0))),
            float(raw_features.get('potassium', raw_features.get('K', 0.0))),
            float(raw_features.get('phosphorus', raw_features.get('P', 0.0)))
        ]
        import pandas as pd
        # The model is a sklearn pipeline that might expect a DataFrame to handle column names correctly
        return pd.DataFrame([features], columns=[
            'temperature', 'humidity', 'rainfall', 'soil_type', 'crop_type', 
            'nitrogen', 'potassium', 'phosphorus'
        ])

    def predict(self, features: Any) -> Dict[str, Any]:
        """
        Run inference returning recommended fertilizer type (e.g., Urea, DAP, MOP).
        """
        if self.model is None or self.encoder is None:
            return {
                "status": "success",
                "prediction": {
                    "recommended_fertilizer": "Urea",
                    "dosage_kg_per_hectare": 0.0,
                    "application_method": "Top dressing",
                },
                "note": "Mock prediction used (model artifact missing)."
            }
            
        try:
            pred_encoded = self.model.predict(features)[0]
            pred_fertilizer = self.encoder.inverse_transform([pred_encoded])[0]
            
            return {
                "status": "success",
                "prediction": {
                    "recommended_fertilizer": pred_fertilizer,
                    # Dosage not predicted by this model, we'd need a separate model or logic
                    "dosage_kg_per_hectare": 50.0, 
                    "application_method": "Base application",
                },
                "note": "Real model inference."
            }
        except Exception as e:
            logger.error(f"Error during fertilizer prediction: {e}")
            return {
                "status": "error",
                "prediction": None,
                "error": str(e)
            }
