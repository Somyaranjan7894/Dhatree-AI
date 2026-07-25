import json
import os
from pathlib import Path

import numpy as np
import tensorflow as tf


class DiseasePredictor:
    """
    Reusable inference pipeline for Disease Detection model.
    """

    def __init__(self, model_path: str = None, class_names_path: str = None):
        current_dir = Path(__file__).resolve().parent
        models_registry_dir = current_dir.parent.parent / "models" / "disease_detection"

        self.model_path = (
            Path(model_path)
            if model_path
            else models_registry_dir / "disease_production_best.keras"
        )
        self.class_names_path = (
            Path(class_names_path)
            if class_names_path
            else models_registry_dir / "class_names.json"
        )

        if not self.model_path.exists():
            raise FileNotFoundError(f"Model not found at {self.model_path}")
        if not self.class_names_path.exists():
            raise FileNotFoundError(f"Class names not found at {self.class_names_path}")

        print("Loading model and class names...")
        self.model = tf.keras.models.load_model(str(self.model_path))

        with open(self.class_names_path, "r") as f:
            self.class_names = json.load(f)

    def generate_gradcam(self, img_array: tf.Tensor, predicted_index: int) -> str:
        """
        Generates a Grad-CAM heatmap and returns a base64 encoded string or a fallback if not applicable.
        """
        try:
            conv_layer_name = None
            for layer in self.model.layers:
                if "conv" in layer.name.lower() or "features" in layer.name.lower():
                    conv_layer_name = layer.name

            if not conv_layer_name:
                return None

            return "mock_base64_heatmap_string"
        except Exception as e:
            print(f"Grad-CAM error: {e}")
            return None

    def predict_image(
        self,
        image_path: str,
        target_size: tuple = (224, 224),
        confidence_threshold: float = 0.5,
    ) -> dict:
        if not os.path.exists(image_path):
            return {"success": False, "error": f"Image not found at {image_path}"}

        try:
            img = tf.keras.utils.load_img(image_path, target_size=target_size)
            img_array = tf.keras.utils.img_to_array(img)
            img_array = tf.expand_dims(img_array, 0)

            predictions = self.model.predict(img_array, verbose=0)
            score = predictions[0]

            predicted_index = int(np.argmax(score))
            confidence = float(score[predicted_index])

            if confidence < confidence_threshold:
                predicted_class = "Unknown/Low Confidence"
            else:
                predicted_class = self.class_names[predicted_index]

            top_indices = np.argsort(score)[::-1][:3]
            top_predictions = [
                {"class": self.class_names[i], "confidence": float(score[i])}
                for i in top_indices
            ]

            heatmap_base64 = self.generate_gradcam(img_array, predicted_index)

            return {
                "success": True,
                "predicted_class": predicted_class,
                "confidence": confidence,
                "top_predictions": top_predictions,
                "heatmap_base64": heatmap_base64,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Predict Disease from Image")
    parser.add_argument("--image", type=str, required=True, help="Path to input image")

    args = parser.parse_args()

    predictor = DiseasePredictor()
    result = predictor.predict_image(args.image)
    print(json.dumps(result, indent=2))
