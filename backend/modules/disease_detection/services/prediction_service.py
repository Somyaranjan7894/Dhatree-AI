import os
import random
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage

from modules.disease_detection.repositories.prediction_repository import (
    DiseasePredictionRepository,
)


class DiseasePredictionService:
    def __init__(self):
        self.repository = DiseasePredictionRepository()

    def _run_inference(self, image_path):
        """
        Runs the actual AI model inference.
        """
        try:
            from ai.disease_detection_backup.predict import DiseasePredictor

            # Paths relative to the project root
            project_root = settings.BASE_DIR.parent
            model_path = (
                project_root
                / "ai"
                / "models"
                / "disease_detection"
                / "disease_production_best.keras"
            )
            class_names_path = (
                project_root
                / "ai"
                / "models"
                / "disease_detection"
                / "class_names.json"
            )

            if not model_path.exists():
                return "Model Not Found", 0.0, {"error": "Production model missing"}

            predictor = DiseasePredictor(str(model_path), str(class_names_path))
            result = predictor.predict_image(str(image_path))

            if result.get("success"):
                metadata = {
                    "top_predictions": result.get("top_predictions", []),
                    "heatmap_base64": result.get("heatmap_base64", None),
                }
                return result.get("predicted_class"), result.get("confidence"), metadata
            else:
                return "Inference Error", 0.0, {"error": result.get("error")}
        except Exception as e:
            return "System Error", 0.0, {"error": str(e)}

    def predict_disease(self, user, image_file, farm=None):
        # 1. Save the initial record to get the file on disk
        prediction = self.repository.create(
            user=user,
            farm=farm,
            image=image_file,
            predicted_class="Processing...",
            confidence_score=0.0,
        )

        # 2. Get absolute path of the saved image
        image_path = Path(settings.MEDIA_ROOT) / str(prediction.image)

        # 3. Perform Inference
        predicted_class, confidence, metadata = self._run_inference(str(image_path))

        # 4. Update the record
        prediction.predicted_class = predicted_class
        prediction.confidence_score = confidence
        prediction.metadata = metadata
        prediction.save()

        return prediction
