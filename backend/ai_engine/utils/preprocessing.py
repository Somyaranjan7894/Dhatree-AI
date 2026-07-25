"""
AI Preprocessing Utilities.
Shared functions for image decoding (OpenCV) and numerical feature scaling (NumPy/Pandas)
used across predictive and vision analysis pipelines.
"""
from typing import List, Optional
import numpy as np

try:
    import cv2
except ImportError:
    cv2 = None  # Fallback handled safely if opencv-python-headless not yet installed in basic dev env


def decode_image_bytes(
    image_bytes: bytes, target_size: tuple[int, int] = (224, 224)
) -> np.ndarray:
    """
    Decode raw byte stream into RGB numpy tensor (`shape: [1, 3, height, width]`).
    Normalizes pixel values from [0, 255] to [0.0, 1.0].
    """
    if cv2 is None:
        raise ImportError(
            "OpenCV is required for image decoding (`opencv-python-headless`)."
        )

    # Decode bytes to BGR image
    nparr = np.frombuffer(image_bytes, np.uint8)
    image_bgr = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image_bgr is None:
        raise ValueError("Could not decode image byte stream. Invalid image format.")

    # Convert BGR to RGB and resize
    image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(image_rgb, target_size, interpolation=cv2.INTER_AREA)

    # Normalize to [0, 1] and transpose to channels-first [C, H, W] then add batch dim [1, C, H, W]
    normalized = resized.astype(np.float32) / 255.0
    transposed = np.transpose(normalized, (2, 0, 1))
    tensor = np.expand_dims(transposed, axis=0)
    return tensor


def normalize_tabular_features(
    raw_values: List[float],
    mean_vector: Optional[List[float]] = None,
    std_vector: Optional[List[float]] = None,
) -> np.ndarray:
    """
    Standardize numerical feature array using Z-score normalization (`(X - mean) / std`).
    """
    arr = np.array(raw_values, dtype=np.float32)
    if mean_vector and std_vector:
        mean = np.array(mean_vector, dtype=np.float32)
        std = np.array(std_vector, dtype=np.float32)
        std[std == 0.0] = 1.0  # Prevent division by zero
        arr = (arr - mean) / std
    return np.expand_dims(arr, axis=0)
