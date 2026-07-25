import os
import joblib
import pandas as pd
import numpy as np
from django.conf import settings

_MODEL_CACHE = None

def _get_model_path():
    try:
        base_dir = settings.BASE_DIR
        return os.path.join(base_dir, '..', 'ai', 'crop_recommendation', 'saved_models', 'best_crop_model.joblib')
    except Exception:
        # Fallback for standalone scripts
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'saved_models', 'best_crop_model.joblib')

def load_model():
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        model_path = _get_model_path()
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model not found at {model_path}. Please train the model first.")
        _MODEL_CACHE = joblib.load(model_path)
    return _MODEL_CACHE

def get_crop_info(crop_name):
    # A simple mock mapping for explanation. In a real app this would be in DB.
    info = {
        'rice': 'Requires high humidity and rainfall.',
        'maize': 'Adaptable to various soils, prefers well-drained loamy soil.',
        'chickpea': 'Grows well in dry, cool conditions.',
        'kidneybeans': 'Requires moderate temperature and rainfall.',
        'pigeonpeas': 'Drought-tolerant, grows well in warm climates.',
        'mothbeans': 'Highly drought resistant, requires little rainfall.',
        'mungbean': 'Warm season crop, needs moderate rainfall.',
        'blackgram': 'Requires warm and humid conditions.',
        'lentil': 'Cool season crop, needs well-drained soil.',
        'pomegranate': 'Tolerates heat and dry conditions well.',
        'banana': 'Needs high humidity, temperature, and rich soil.',
        'mango': 'Prefers warm climates, tolerates varied soils.',
        'grapes': 'Needs dry heat during ripening, well-drained soil.',
        'watermelon': 'Requires warm weather and sandy loam soil.',
        'muskmelon': 'Prefers warm temperatures and lots of sunlight.',
        'apple': 'Requires a cool climate and chilling hours.',
        'orange': 'Needs subtropical to tropical climate.',
        'papaya': 'Tropical crop, sensitive to frost and waterlogging.',
        'coconut': 'Coastal crop, high humidity and regular rainfall.',
        'cotton': 'Requires warm climate and moderate rainfall.',
        'jute': 'Hot and humid climate with heavy rainfall needed.',
        'coffee': 'Requires cool, moist climate with well-drained soil.'
    }
    return info.get(crop_name.lower(), "Optimal conditions matched.")

def predict_crop(n, p, k, temperature, humidity, ph, rainfall):
    pipeline = load_model()
    
    # Feature names must match what was used during training
    input_data = pd.DataFrame([[n, p, k, temperature, humidity, ph, rainfall]], 
                              columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
    
    # Get probabilities if the classifier supports it (RandomForest does)
    try:
        probabilities = pipeline.predict_proba(input_data)[0]
        classes = pipeline.classes_
        
        # Sort classes by probability descending
        sorted_indices = np.argsort(probabilities)[::-1]
        top_3_indices = sorted_indices[:3]
        
        results = []
        for idx in top_3_indices:
            crop = classes[idx]
            conf = probabilities[idx]
            if conf > 0:
                results.append({
                    "crop": crop,
                    "confidence": float(conf),
                    "explanation": get_crop_info(crop)
                })
        
        best_crop = results[0]
        alternatives = results[1:] if len(results) > 1 else []
        
        return {
            "recommended_crop": best_crop["crop"],
            "confidence_score": best_crop["confidence"],
            "explanation": best_crop["explanation"],
            "alternatives": alternatives
        }
        
    except AttributeError:
        # Fallback if the model doesn't support predict_proba (e.g. standard SVM without probability=True)
        prediction = pipeline.predict(input_data)[0]
        return {
            "recommended_crop": prediction,
            "confidence_score": 1.0,
            "explanation": get_crop_info(prediction),
            "alternatives": []
        }
