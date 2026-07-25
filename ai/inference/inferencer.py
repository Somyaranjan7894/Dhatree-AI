import torch
import numpy as np
from typing import Dict, Any, List
from ai.utils.logger import ai_logger
from ai.preprocessing.image_processor import BaseImageProcessor
from ai.models.model_manager import ModelManager

class BaseInferencer:
    """
    Reusable inference pipeline.
    Handles model loading, image preprocessing, safe prediction execution, and postprocessing.
    """
    def __init__(self, model: torch.nn.Module, model_manager: ModelManager, 
                 model_name: str, processor: BaseImageProcessor, 
                 class_names: List[str], use_gpu: bool = True):
        self.device = torch.device("cuda" if use_gpu and torch.cuda.is_available() else "cpu")
        self.model = model.to(self.device)
        self.processor = processor
        self.class_names = class_names
        
        # Load the latest best checkpoint
        best_model_path = model_manager.models_dir / f"{model_name}_best.pth"
        if best_model_path.exists():
            model_manager.load_model(self.model, str(best_model_path))
        else:
            ai_logger.warning(f"No best model found at {best_model_path}. Inference will use uninitialized weights unless loaded manually.")
            
        self.model.eval()

    def predict(self, image_path_or_bytes: Any) -> Dict[str, Any]:
        """
        Executes a single image prediction through the network.
        Returns confidence scores for top predictions.
        """
        try:
            # 1. Preprocess
            tensor = self.processor.preprocess_image(image_path_or_bytes, is_training=False)
            
            # Add batch dimension (B, C, H, W) and move to device
            tensor = tensor.unsqueeze(0).to(self.device)
            
            # 2. Inference
            with torch.no_grad():
                outputs = self.model(tensor)
                
                # 3. Postprocess (Softmax to get probabilities)
                probabilities = torch.nn.functional.softmax(outputs, dim=1)[0]
                
            probs_np = probabilities.cpu().numpy()
            predicted_idx = np.argmax(probs_np)
            predicted_class = self.class_names[predicted_idx]
            confidence = float(probs_np[predicted_idx])
            
            # Build detailed report
            class_probs = {self.class_names[i]: float(probs_np[i]) for i in range(len(self.class_names))}
            
            return {
                "predicted_class": predicted_class,
                "confidence": confidence,
                "all_probabilities": class_probs,
                "success": True
            }
            
        except Exception as e:
            ai_logger.error(f"Inference failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
