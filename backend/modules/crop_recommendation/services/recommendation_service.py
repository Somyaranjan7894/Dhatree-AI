import os
import sys

from django.conf import settings

from modules.crop_recommendation.repositories.recommendation_repository import (
    CropRecommendationRepository,
)


class CropRecommendationService:
    def __init__(self):
        self.repository = CropRecommendationRepository()

    def predict_crop(self, user, data, farm=None):
        from ai_engine.pipelines.crop_recommendation.pipeline import CropRecommendationPipeline
        
        pipeline = CropRecommendationPipeline()
        features = pipeline.preprocess({
            "nitrogen": data["nitrogen"],
            "phosphorus": data["phosphorus"],
            "potassium": data["potassium"],
            "temperature": data["temperature"],
            "humidity": data["humidity"],
            "ph": data["ph"],
            "rainfall": data["rainfall"],
        })
        result = pipeline.predict(features)
        
        if result["status"] == "success":
            pred_data = result["prediction"]
            recommended_crop = pred_data.get("recommended_crop")
            confidence_score = pred_data.get("confidence_score", 0.0)
            alternatives = pred_data.get("alternatives", [])
            explanation = result.get("note", "")
        else:
            recommended_crop = "Unknown"
            confidence_score = 0.0
            alternatives = []
            explanation = "Error: " + result.get("error", "Unknown error")

        # Save to DB
        prediction = self.repository.create(
            user=user,
            farm=farm,
            nitrogen=data["nitrogen"],
            phosphorus=data["phosphorus"],
            potassium=data["potassium"],
            ph=data["ph"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            rainfall=data["rainfall"],
            recommended_crop=recommended_crop,
            confidence_score=confidence_score,
            alternatives=alternatives,
            explanation=explanation,
            model_version="v1.0-RF",
        )

        return prediction
