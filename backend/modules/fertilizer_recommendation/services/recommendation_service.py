import logging
from typing import Dict, Any
from ai.fertilizer_recommendation.predict import FertilizerPredictor
from modules.fertilizer_recommendation.models.recommendation import FertilizerRecommendation

logger = logging.getLogger(__name__)
predictor_instance = None

def get_predictor():
    global predictor_instance
    if predictor_instance is None:
        try:
            predictor_instance = FertilizerPredictor()
        except Exception as e:
            logger.error(f"Failed to initialize FertilizerPredictor: {e}")
            raise
    return predictor_instance

class FertilizerRecommendationService:
    @staticmethod
    def predict_fertilizer(user, data: Dict[str, Any]) -> FertilizerRecommendation:
        """
        Runs the AI model and saves the prediction to the database.
        """
        predictor = get_predictor()
        
        # Prepare inputs
        ai_inputs = {
            "nitrogen": data.get("nitrogen"),
            "phosphorus": data.get("phosphorus"),
            "potassium": data.get("potassium"),
            "temperature": data.get("temperature"),
            "humidity": data.get("humidity"),
            "rainfall": data.get("rainfall"),
            "ph_level": data.get("ph_level"),
            "crop_type": data.get("crop_type"),
            "soil_type": data.get("soil_type")
        }
        
        # Get threshold from config or default
        confidence_threshold = data.get("confidence_threshold", 0.5)
        
        # Run inference
        prediction_result = predictor.predict(ai_inputs, confidence_threshold=confidence_threshold)
        
        # Build metadata
        metadata = {
            "alternatives": prediction_result.get("alternatives", []),
            "model_version": "v1.0.0" # Hardcoded for now, could be fetched from predictor
        }
        
        # Save to DB
        recommendation = FertilizerRecommendation.objects.create(
            user=user,
            farm_id=data.get("farm"),
            crop_type=data.get("crop_type"),
            nitrogen=data.get("nitrogen"),
            phosphorus=data.get("phosphorus"),
            potassium=data.get("potassium"),
            ph_level=data.get("ph_level"),
            temperature=data.get("temperature"),
            humidity=data.get("humidity"),
            rainfall=data.get("rainfall"),
            soil_type=data.get("soil_type", "Unknown"),
            recommended_fertilizer=prediction_result.get("recommended_fertilizer"),
            confidence_score=prediction_result.get("confidence_score", 0.0),
            explanation=prediction_result.get("explanation"),
            application_guidance=prediction_result.get("application_guidance"),
            warnings=prediction_result.get("warnings"),
            metadata=metadata
        )
        
        return recommendation
