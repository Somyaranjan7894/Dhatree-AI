import os
import torch
import json
from pathlib import Path
from typing import Dict, Optional, Any
from ai.utils.logger import ai_logger

class ModelManager:
    """
    Utilities for managing the lifecycle of saved AI models.
    Supports saving, loading, versioning, and best model selection.
    """
    
    def __init__(self, models_dir: str):
        self.models_dir = Path(models_dir)
        self.models_dir.mkdir(parents=True, exist_ok=True)
        
    def save_model(self, model: torch.nn.Module, optimizer: torch.optim.Optimizer, 
                   epoch: int, metrics: Dict[str, float], model_name: str, is_best: bool = False):
        """
        Saves a model checkpoint along with its training state and metadata.
        """
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'metrics': metrics
        }
        
        # Save standard versioned checkpoint
        version = f"v{epoch:03d}"
        model_path = self.models_dir / f"{model_name}_{version}.pth"
        torch.save(checkpoint, model_path)
        ai_logger.info(f"Saved model checkpoint to {model_path}")
        
        # Save metadata
        metadata_path = self.models_dir / f"{model_name}_{version}_meta.json"
        with open(metadata_path, 'w') as f:
            json.dump({'epoch': epoch, 'metrics': metrics}, f, indent=4)
            
        # If it's the best model, save a copy as "best"
        if is_best:
            best_path = self.models_dir / f"{model_name}_best.pth"
            torch.save(checkpoint, best_path)
            ai_logger.info(f"Updated best model at {best_path} with metrics {metrics}")

    def load_model(self, model: torch.nn.Module, model_path: str, optimizer: Optional[torch.optim.Optimizer] = None) -> Dict[str, Any]:
        """
        Loads a saved model checkpoint into a PyTorch model.
        Returns the checkpoint dictionary containing epoch and metrics.
        """
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found: {path}")
            
        ai_logger.info(f"Loading model checkpoint from {path}")
        checkpoint = torch.load(path, map_location=torch.device('cpu')) # load to cpu by default, let trainer move to GPU
        
        model.load_state_dict(checkpoint['model_state_dict'])
        if optimizer and 'optimizer_state_dict' in checkpoint:
            optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
            
        return checkpoint

    def get_latest_checkpoint(self, model_name: str) -> Optional[Path]:
        """
        Finds the latest versioned checkpoint for a given model name.
        """
        checkpoints = list(self.models_dir.glob(f"{model_name}_v*.pth"))
        if not checkpoints:
            return None
            
        # Sort by version number
        checkpoints.sort(key=lambda x: x.name)
        return checkpoints[-1]
