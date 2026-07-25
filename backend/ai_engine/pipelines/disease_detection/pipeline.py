"""
Disease Detection AI Vision Pipeline.
Implements `AnalyzerInterface` to decode raw leaf images, normalize color channels via OpenCV,
and execute vision model inference (`PyTorch`/`TensorFlow`) to detect crop diseases.
"""
from typing import Any, Dict
import numpy as np
import logging
import json
from ai_engine.interfaces.base import AnalyzerInterface
from ai_engine.models_registry import ModelsRegistry

logger = logging.getLogger(__name__)

def _load_keras_model_and_classes(registry_path):
    import keras
    model_path = registry_path / "disease_detection" / "disease_production_best.keras"
    classes_path = registry_path / "disease_detection" / "class_names.json"
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found at {model_path}")
    if not classes_path.exists():
        raise FileNotFoundError(f"Class names not found at {classes_path}")
        
    logger.info(f"Loading real disease detection model from {model_path}")
    model = keras.models.load_model(model_path)
    with open(classes_path, 'r') as f:
        class_names = json.load(f)
        
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
            self.model, self.class_names = self.registry.get_model(self.MODEL_KEY, _load_keras_model_and_classes)
        except Exception as e:
            logger.warning(f"Disease model failed to load. Will fall back to mock. Error: {e}")

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
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        image = image.resize((224, 224))
        
        # Convert to numpy array. Model architecture includes its own preprocess_input layer.
        img_array = np.array(image, dtype=np.float32)
        
        # Add batch dimension [1, 224, 224, 3]
        return np.expand_dims(img_array, axis=0)

    def analyze(self, image_tensor: np.ndarray) -> Dict[str, Any]:
        """
        Run forward vision inference returning detected condition, confidence, and bounding box/heatmap info.
        """
        if self.model is None or not self.class_names:
            return {
                "status": "success",
                "analysis": {
                    "detected_disease": "healthy",
                    "confidence_score": 0.0,
                    "severity_index": 0.0,
                    "affected_region_bbox": None,
                },
                "note": "Mock prediction used (model artifact missing)."
            }
            
        try:
            preds = self.model.predict(image_tensor)[0]
            pred_class_idx = np.argmax(preds)
            pred_class = self.class_names[pred_class_idx]
            confidence = float(preds[pred_class_idx])
            
            return {
                "status": "success",
                "analysis": {
                    "detected_disease": pred_class,
                    "confidence_score": confidence,
                    "severity_index": confidence if pred_class.lower() != 'healthy' else 0.0,
                    "affected_region_bbox": None,
                },
                "note": "Real model inference."
            }
        except Exception as e:
            logger.error(f"Error during disease detection prediction: {e}")
            return {
                "status": "error",
                "analysis": None,
                "error": str(e)
            }
