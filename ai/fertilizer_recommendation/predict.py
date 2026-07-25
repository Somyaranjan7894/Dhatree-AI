import json
import logging
from pathlib import Path
import joblib
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

ARTIFACTS_DIR = Path("ai/models/artifacts")
MODEL_PATH = ARTIFACTS_DIR / "fertilizer_production_best.joblib"
ENCODER_PATH = ARTIFACTS_DIR / "fertilizer_label_encoder.joblib"
REGISTRY_PATH = Path("ai/models/fertilizer_training_registry.json")

class FertilizerPredictor:
    def __init__(self):
        self.model = None
        self.encoder = None
        self.target_classes = []
        self._load_model()
        
    def _load_model(self):
        try:
            if MODEL_PATH.exists() and ENCODER_PATH.exists():
                self.model = joblib.load(MODEL_PATH)
                self.encoder = joblib.load(ENCODER_PATH)
                if REGISTRY_PATH.exists():
                    with open(REGISTRY_PATH, 'r') as f:
                        registry = json.load(f)
                        self.target_classes = registry.get("target_classes", list(self.encoder.classes_))
                else:
                    self.target_classes = list(self.encoder.classes_)
                logging.info("Fertilizer model and encoder loaded successfully.")
            else:
                logging.warning("Fertilizer model or encoder not found. Running in mock mode.")
        except Exception as e:
            logging.error(f"Error loading model: {e}")
            
    def predict(self, input_data: dict, confidence_threshold=0.5):
        """
        input_data should be a dict with keys:
        temperature, humidity, rainfall, nitrogen, potassium, phosphorus, soil_type, crop_type
        """
        if self.model is None or self.encoder is None:
            # Return mock prediction for testing/setup
            return self._mock_predict(input_data)
            
        try:
            df = pd.DataFrame([input_data])
            
            # Predict probabilities if model supports it
            if hasattr(self.model, "predict_proba"):
                probas = self.model.predict_proba(df)[0]
                
                # Get indices sorted by probability descending
                top_indices = np.argsort(probas)[::-1]
                
                predictions = []
                for idx in top_indices:
                    prob = float(probas[idx])
                    if prob > 0:
                        pred_class = self.encoder.inverse_transform([idx])[0]
                        predictions.append({"fertilizer": pred_class, "confidence": prob})
                        
                if not predictions:
                    return self._fallback_prediction()
                    
                top_pred = predictions[0]
                if top_pred["confidence"] < confidence_threshold:
                    return {
                        "recommended_fertilizer": "Unknown - Low Confidence",
                        "confidence_score": top_pred["confidence"],
                        "alternatives": predictions[1:4],
                        "explanation": "The AI could not determine a suitable fertilizer with high confidence based on the provided soil and weather conditions.",
                        "application_guidance": "Consult a local agronomist.",
                        "warnings": "Do not apply unknown fertilizers."
                    }
                    
                return {
                    "recommended_fertilizer": top_pred["fertilizer"],
                    "confidence_score": top_pred["confidence"],
                    "alternatives": predictions[1:4],
                    "explanation": f"Based on the soil NPK levels and {input_data.get('crop_type', 'your crop')}, {top_pred['fertilizer']} is highly recommended.",
                    "application_guidance": "Apply evenly across the soil base during the early growth phase.",
                    "warnings": "Avoid over-application as it may lead to soil toxicity."
                }
            else:
                # Fallback to direct prediction
                pred = self.model.predict(df)[0]
                pred_class = self.encoder.inverse_transform([pred])[0]
                return {
                    "recommended_fertilizer": pred_class,
                    "confidence_score": 1.0, # Unknown actual probability
                    "alternatives": [],
                    "explanation": f"Based on the input parameters, {pred_class} is the recommended fertilizer.",
                    "application_guidance": "Apply according to standard practices for this crop.",
                    "warnings": None
                }
                
        except Exception as e:
            logging.error(f"Prediction failed: {e}")
            raise RuntimeError(f"Fertilizer prediction failed: {str(e)}")

    def _fallback_prediction(self):
         return {
            "recommended_fertilizer": "Unknown",
            "confidence_score": 0.0,
            "alternatives": [],
            "explanation": "Unable to generate a valid prediction.",
            "application_guidance": None,
            "warnings": None
        }

    def _mock_predict(self, input_data: dict):
        logging.info(f"Mock predicting for input: {input_data}")
        # A smart mock that changes based on NPK
        n, p, k = input_data.get('nitrogen', 0), input_data.get('phosphorus', 0), input_data.get('potassium', 0)
        
        if n > p and n > k:
            fert = "Urea"
        elif p > n and p > k:
            fert = "DAP"
        elif k > n and k > p:
            fert = "MOP"
        else:
            fert = "14-35-14"
            
        return {
            "recommended_fertilizer": fert,
            "confidence_score": 0.85,
            "alternatives": [{"fertilizer": "10-26-26", "confidence": 0.10}],
            "explanation": f"Since the dominant nutrient required is modeled as {fert}, it is the primary recommendation. (MOCK MODE)",
            "application_guidance": "Apply 50kg per hectare. Incorporate into soil before sowing.",
            "warnings": "Ensure soil moisture is adequate before application."
        }
