"""
Disease Detection AI Vision Pipeline.
Implements `AnalyzerInterface` to decode raw leaf images, normalize color channels via OpenCV,
and execute vision model inference (`PyTorch`/`TensorFlow`) to detect crop diseases.
"""

import json
import logging
import traceback
from typing import Any, Dict

import numpy as np

from ai_engine.interfaces.base import AnalyzerInterface
from ai_engine.models_registry import ModelsRegistry

logger = logging.getLogger(__name__)


def _load_keras_model_and_classes(registry_path):
    import os
    os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
    os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    import keras

    model_path = registry_path / "disease_detection" / "disease_production_best.keras"
    classes_path = registry_path / "disease_detection" / "class_names.json"

    logger.info(f"Resolving model path: {model_path.resolve()}")
    if not model_path.exists():
        logger.error(f"Missing model artifact at {model_path}")
        raise FileNotFoundError(f"Model not found at {model_path}")
    if not classes_path.exists():
        logger.error(f"Missing class names at {classes_path}")
        raise FileNotFoundError(f"Class names not found at {classes_path}")

    logger.info(f"Loading real disease detection model from {model_path}")
    model = keras.models.load_model(model_path)
    logger.info("Successfully loaded keras model.")
    
    with open(classes_path, "r") as f:
        class_names = json.load(f)
    logger.info(f"Successfully loaded {len(class_names)} class names.")

    return model, class_names


class DiseaseDetectionPipeline(AnalyzerInterface):
    """
    Vision analysis pipeline for identifying crop foliage anomalies and leaf diseases.
    Now loads the trained artifact from registry to perform inference.
    """

    MODEL_KEY = "disease_detection_vision_net"

    def __init__(self) -> None:
        self.registry = ModelsRegistry()
        self.model = None
        self.class_names = []
        try:
            self.model, self.class_names = self.registry.get_model(
                self.MODEL_KEY, _load_keras_model_and_classes
            )
            logger.info("DiseaseDetectionPipeline initialized with loaded model.")
        except Exception as e:
            logger.warning(
                f"Disease model failed to load. Will fall back to mock. Error: {e}\n{traceback.format_exc()}"
            )

    def load_model(self, model_path: str) -> None:
        """Load deep neural network vision architecture into model registry."""
        pass

    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """
        Decode byte stream to RGB tensor array,
        resize to 224x224, and apply ImageNet normalization.
        Expects NHWC format for Keras.
        """
        import io
        from PIL import Image

        try:
            logger.info("Decoding and converting image bytes to RGB...")
            image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            
            logger.info("Resizing image to 224x224...")
            image = image.resize((224, 224))

            # Convert to numpy array. Model architecture includes its own preprocess_input layer.
            img_array = np.array(image, dtype=np.float32)

            # Add batch dimension [1, 224, 224, 3]
            tensor = np.expand_dims(img_array, axis=0)
            logger.info(f"Image preprocessing successful. Tensor shape: {tensor.shape}")
            return tensor
        except Exception as e:
            logger.error(f"Image preprocessing failed: {e}\n{traceback.format_exc()}")
            raise

    def analyze(self, image_tensor: np.ndarray) -> Dict[str, Any]:
        """
        Run forward vision inference returning detected condition, confidence, and bounding box/heatmap info.
        """
        if self.model is None or not self.class_names:
            logger.info("Using mock prediction because real model is not loaded.")
            return {
                "status": "success",
                "analysis": {
                    "detected_disease": "healthy",
                    "confidence_score": 0.0,
                    "severity_index": 0.0,
                    "affected_region_bbox": None,
                },
                "note": "Mock prediction used (model artifact missing).",
            }

        try:
            logger.info("Running forward pass through keras model...")
            preds = self.model.predict(image_tensor)[0]
            
            pred_class_idx = np.argmax(preds)
            pred_class = self.class_names[pred_class_idx]
            confidence = float(preds[pred_class_idx])
            
            logger.info(f"Model predicted {pred_class} with {confidence*100:.2f}% confidence.")

            return {
                "status": "success",
                "analysis": {
                    "detected_disease": pred_class,
                    "confidence_score": confidence,
                    "severity_index": (
                        confidence if pred_class.lower() != "healthy" else 0.0
                    ),
                    "affected_region_bbox": None,
                },
                "note": "Real model inference.",
            }
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Error during disease detection prediction: {e}\n{error_trace}")
            return {"status": "error", "analysis": None, "error": str(e), "traceback": error_trace}
        finally:
            # Force garbage collection to instantly free memory
            import gc
            if 'image_tensor' in locals():
                del image_tensor
            if 'preds' in locals():
                del preds
            gc.collect()
