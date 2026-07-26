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
            from ai_engine.pipelines.disease_detection.pipeline import DiseaseDetectionPipeline
            
            pipeline = DiseaseDetectionPipeline()
            
            with open(image_path, "rb") as f:
                image_bytes = f.read()
                
            features = pipeline.preprocess_image(image_bytes)
            result = pipeline.analyze(features)
            
            if result["status"] == "success":
                pred = result["analysis"]
                metadata = {
                    "top_predictions": result.get("note", ""),
                    "heatmap_base64": pred.get("affected_region_bbox", None),
                }
                return pred.get("detected_disease", "Unknown"), pred.get("confidence_score", 0.0), metadata
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
