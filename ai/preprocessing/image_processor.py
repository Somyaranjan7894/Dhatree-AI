import torch
from torchvision import transforms
from PIL import Image
from typing import Tuple, Union
import numpy as np

class BaseImageProcessor:
    """
    Reusable image preprocessing utilities for AI pipelines.
    Handles resizing, normalization, and tensor conversion safely.
    """
    
    def __init__(self, target_size: Tuple[int, int] = (224, 224), 
                 mean: Tuple[float, float, float] = (0.485, 0.456, 0.406), 
                 std: Tuple[float, float, float] = (0.229, 0.224, 0.225)):
        self.target_size = target_size
        self.mean = mean
        self.std = std
        
        # Standard torchvision transform for inference/validation
        self.transform = transforms.Compose([
            transforms.Resize(self.target_size),
            transforms.ToTensor(),
            transforms.Normalize(mean=self.mean, std=self.std)
        ])
        
        # Transform for training with basic augmentations
        self.train_transform = transforms.Compose([
            transforms.RandomResizedCrop(self.target_size),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
            transforms.Normalize(mean=self.mean, std=self.std)
        ])

    def preprocess_image(self, image: Union[str, Image.Image, np.ndarray], is_training: bool = False) -> torch.Tensor:
        """
        Processes a raw image path, PIL Image, or Numpy array into a normalized PyTorch tensor.
        """
        # Convert to PIL Image if necessary
        if isinstance(image, str):
            img = Image.open(image)
        elif isinstance(image, np.ndarray):
            img = Image.fromarray(image)
        else:
            img = image
            
        # Ensure RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        # Apply transformation
        if is_training:
            tensor = self.train_transform(img)
        else:
            tensor = self.transform(img)
            
        return tensor
        
    def denormalize(self, tensor: torch.Tensor) -> np.ndarray:
        """
        Reverses the normalization on a tensor to return it to [0, 1] for visualization.
        """
        # Clone to avoid modifying the original
        tensor = tensor.clone()
        for t, m, s in zip(tensor, self.mean, self.std):
            t.mul_(s).add_(m)
            
        # Clamp to [0, 1] just in case
        tensor = torch.clamp(tensor, 0, 1)
        
        # Convert to numpy (H, W, C)
        img_np = tensor.permute(1, 2, 0).cpu().numpy()
        return img_np
