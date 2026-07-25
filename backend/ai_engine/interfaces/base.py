"""
Abstract AI/ML Interfaces.
Ensures uniform contract across all prediction pipelines (`PredictorInterface`)
and vision/image analysis pipelines (`AnalyzerInterface`).
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Union

import numpy as np


class PredictorInterface(ABC):
    """
    Interface for tabular and numerical predictive models
    (e.g., Crop Recommendation, Fertilizer Recommendation, Yield Prediction).
    """

    @abstractmethod
    def load_model(self, model_path: str) -> None:
        """Load trained model weights or artifacts from disk/memory registry."""
        pass

    @abstractmethod
    def preprocess(self, raw_features: Dict[str, Any]) -> np.ndarray:
        """Transform raw input dictionaries into model-ready feature arrays."""
        pass

    @abstractmethod
    def predict(self, features: np.ndarray) -> Dict[str, Any]:
        """Run forward inference and output standardized probability/confidence results."""
        pass

    def execute_pipeline(self, raw_features: Dict[str, Any]) -> Dict[str, Any]:
        """Orchestrate preprocessing, inference, and postprocessing."""
        processed = self.preprocess(raw_features)
        return self.predict(processed)


class AnalyzerInterface(ABC):
    """
    Interface for vision and deep learning image classification/segmentation models
    (e.g., Disease Detection, Disease Diagnosis).
    """

    @abstractmethod
    def load_model(self, model_path: str) -> None:
        """Load deep learning vision model (`PyTorch`/`TensorFlow`/`ONNX`)."""
        pass

    @abstractmethod
    def preprocess_image(self, image_bytes: bytes) -> np.ndarray:
        """Decode and normalize raw image byte stream using OpenCV/PIL into tensor array."""
        pass

    @abstractmethod
    def analyze(self, image_tensor: np.ndarray) -> Dict[str, Any]:
        """Execute vision inference returning detected conditions, bounding boxes, or diagnosis."""
        pass

    def execute_vision_pipeline(self, image_bytes: bytes) -> Dict[str, Any]:
        """Orchestrate image decoding, resizing, vision inference, and result mapping."""
        tensor = self.preprocess_image(image_bytes)
        return self.analyze(tensor)
