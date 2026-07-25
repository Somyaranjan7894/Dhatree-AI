import pytest
from pathlib import Path
from PIL import Image
from ai.config.settings import config, AIConfig

try:
    import torch
    import torch.nn as nn
    import numpy as np
    from ai.preprocessing.image_processor import BaseImageProcessor
    from ai.evaluation.evaluator import ModelEvaluator
    from ai.models.model_manager import ModelManager
    HAS_AI_LIBS = True
except ImportError:
    HAS_AI_LIBS = False

def test_config_initialization():
    """Ensure config paths resolve correctly"""
    assert config.model.image_size == (224, 224)
    assert config.dataset.raw_dir.exists()
    assert config.model.models_dir.exists()

@pytest.mark.skipif(not HAS_AI_LIBS, reason="Torch/sklearn not installed")
def test_image_processor():
    """Test image preprocessing to tensor"""
    processor = BaseImageProcessor(target_size=(128, 128))
    
    # Create dummy image
    dummy_img = Image.new('RGB', (256, 256), color = 'red')
    
    tensor = processor.preprocess_image(dummy_img)
    
    # Assertions
    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == (3, 128, 128)

@pytest.mark.skipif(not HAS_AI_LIBS, reason="Torch/sklearn not installed")
def test_evaluator_metrics():
    """Test standard evaluation maths using scikit-learn"""
    y_true = [0, 1, 0, 1, 1, 0]
    y_pred = [0, 1, 0, 0, 1, 1]
    
    eval_results = ModelEvaluator.evaluate_classification(y_true, y_pred, target_names=["Class A", "Class B"])
    metrics = eval_results["metrics"]
    
    assert "accuracy" in metrics
    assert "f1_score" in metrics
    assert metrics["accuracy"] == 4.0 / 6.0

@pytest.mark.skipif(not HAS_AI_LIBS, reason="Torch/sklearn not installed")
def test_model_manager_saving(tmp_path):
    """Test saving functionality of ModelManager"""
    manager = ModelManager(str(tmp_path))
    dummy_model = nn.Linear(10, 2)
    dummy_optimizer = torch.optim.SGD(dummy_model.parameters(), lr=0.01)
    metrics = {"val_loss": 0.5}
    
    # Save standard
    manager.save_model(dummy_model, dummy_optimizer, 1, metrics, "test_model", is_best=True)
    
    assert (tmp_path / "test_model_v001.pth").exists()
    assert (tmp_path / "test_model_v001_meta.json").exists()
    assert (tmp_path / "test_model_best.pth").exists()
