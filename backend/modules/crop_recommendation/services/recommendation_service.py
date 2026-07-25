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
        # We need to invoke the AI module. Since it's in the Django path, we can import it directly.
        # But to keep decoupled, we import it inside the method or add the root path if necessary.

        root_dir = os.path.abspath(os.path.join(settings.BASE_DIR, ".."))
        if root_dir not in sys.path:
            sys.path.insert(0, root_dir)

        from ai.crop_recommendation.predict import predict_crop

        result = predict_crop(
            n=data["nitrogen"],
            p=data["phosphorus"],
            k=data["potassium"],
            temperature=data["temperature"],
            humidity=data["humidity"],
            ph=data["ph"],
            rainfall=data["rainfall"],
        )

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
            recommended_crop=result["recommended_crop"],
            confidence_score=result["confidence_score"],
            alternatives=result["alternatives"],
            explanation=result["explanation"],
            model_version="v1.0-RF",
        )

        return prediction
