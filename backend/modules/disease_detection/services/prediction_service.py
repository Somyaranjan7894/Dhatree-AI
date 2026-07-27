import logging
import traceback
from pathlib import Path

from django.conf import settings
from django.core.files.storage import default_storage

from modules.disease_detection.repositories.prediction_repository import (
    DiseasePredictionRepository,
)

logger = logging.getLogger(__name__)


class DiseasePredictionService:
    def __init__(self):
        self.repository = DiseasePredictionRepository()

    def _run_inference(self, image_bytes):
        """
        Runs the actual AI model inference directly from memory.
        """
        try:
            logger.info("Initializing DiseaseDetectionPipeline...")
            from ai_engine.pipelines.disease_detection.pipeline import (
                DiseaseDetectionPipeline,
            )

            pipeline = DiseaseDetectionPipeline()

            logger.info("Preprocessing image bytes...")
            features = pipeline.preprocess_image(image_bytes)
            
            logger.info("Analyzing image features...")
            result = pipeline.analyze(features)

            if result["status"] == "success":
                pred = result["analysis"]
                metadata = {
                    "top_predictions": result.get("note", ""),
                    "heatmap_base64": pred.get("affected_region_bbox", None),
                }
                logger.info(f"Inference success: {pred.get('detected_disease')}")
                return (
                    pred.get("detected_disease", "Unknown"),
                    pred.get("confidence_score", 0.0),
                    metadata,
                )
            else:
                logger.error(f"Inference Pipeline Error: {result.get('error')}")
                return "Inference Error", 0.0, {"error": result.get("error")}
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"System Error during inference:\n{error_trace}")
            return "System Error", 0.0, {"error": str(e), "traceback": error_trace}

    def predict_disease(self, user, image_file, farm=None):
        logger.info(f"Starting disease prediction for user: {user.username}")
        # 1. Save the initial record
        prediction = self.repository.create(
            user=user,
            farm=farm,
            image=image_file,
            predicted_class="Processing...",
            confidence_score=0.0,
        )
        logger.info(f"Created initial prediction record: {prediction.id}")

        # 2. Get image bytes directly from uploaded file to avoid local path resolution issues with Cloudinary
        logger.info("Reading image bytes from uploaded file...")
        image_file.seek(0)
        image_bytes = image_file.read()

        # 3. Perform Inference
        logger.info("Running inference...")
        predicted_class, confidence, metadata = self._run_inference(image_bytes)

        # 4. Update the record
        prediction.predicted_class = predicted_class
        prediction.confidence_score = confidence
        prediction.metadata = metadata
        prediction.save()
        logger.info(f"Updated prediction record: {prediction.id} with class: {predicted_class}")

        return prediction
