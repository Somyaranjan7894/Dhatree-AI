import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import Tuple

# Get the absolute root directory of the `ai/` folder
AI_BASE_DIR = Path(__file__).resolve().parent.parent

@dataclass
class ModelConfig:
    """Configuration for AI models"""
    # Architecture
    image_size: Tuple[int, int] = (224, 224)
    num_classes: int = 10
    
    # Training defaults
    batch_size: int = 32
    epochs: int = 50
    learning_rate: float = 1e-4
    
    # Paths
    models_dir: Path = AI_BASE_DIR / "models" / "artifacts"
    
    def __post_init__(self):
        self.models_dir.mkdir(parents=True, exist_ok=True)

@dataclass
class DatasetConfig:
    """Configuration for Datasets"""
    raw_dir: Path = AI_BASE_DIR / "datasets" / "raw"
    processed_dir: Path = AI_BASE_DIR / "datasets" / "processed"
    metadata_dir: Path = AI_BASE_DIR / "datasets" / "metadata"
    sample_dir: Path = AI_BASE_DIR / "datasets" / "sample"
    
    def __post_init__(self):
        self.raw_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
        self.sample_dir.mkdir(parents=True, exist_ok=True)

@dataclass
class AIConfig:
    """Global AI Environment Configuration"""
    model: ModelConfig = field(default_factory=ModelConfig)
    dataset: DatasetConfig = field(default_factory=DatasetConfig)
    
    # Global flags
    use_gpu: bool = True
    seed: int = 42

# Global configuration instance
config = AIConfig()
