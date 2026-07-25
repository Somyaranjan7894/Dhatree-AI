import os
import json
from pathlib import Path
from PIL import Image
from typing import Dict, List, Tuple
from torchvision.datasets import ImageFolder
from torch.utils.data import DataLoader, Dataset
from ai.utils.logger import ai_logger

class DatasetManager:
    """
    Reusable utilities for loading and validating image datasets.
    """
    def __init__(self, dataset_path: str):
        self.dataset_path = Path(dataset_path)
        
    def validate_dataset(self) -> Dict[str, any]:
        """
        Scans the dataset directory, detects corrupted images, and counts classes/instances.
        """
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset path not found: {self.dataset_path}")

        classes = [d.name for d in self.dataset_path.iterdir() if d.is_dir()]
        report = {
            "path": str(self.dataset_path),
            "total_classes": len(classes),
            "classes": classes,
            "class_counts": {},
            "total_images": 0,
            "corrupted_images": []
        }
        
        for cls_name in classes:
            cls_dir = self.dataset_path / cls_name
            img_files = [f for f in cls_dir.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png']]
            valid_count = 0
            
            for img_file in img_files:
                try:
                    with Image.open(img_file) as img:
                        img.verify() # Verify image integrity
                    valid_count += 1
                except Exception as e:
                    ai_logger.warning(f"Corrupted image found: {img_file} - {e}")
                    report["corrupted_images"].append(str(img_file))
            
            report["class_counts"][cls_name] = valid_count
            report["total_images"] += valid_count
            
        ai_logger.info(f"Dataset Validation Complete: {report['total_images']} valid images across {report['total_classes']} classes.")
        if report["corrupted_images"]:
            ai_logger.error(f"Found {len(report['corrupted_images'])} corrupted images.")
            
        return report

    def save_metadata(self, report: Dict[str, any], output_path: str):
        """
        Saves dataset summary/metadata to a JSON file.
        """
        out_file = Path(output_path)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        with open(out_file, 'w') as f:
            json.dump(report, f, indent=4)
        ai_logger.info(f"Dataset metadata saved to {out_file}")

    def get_dataloader(self, transform, batch_size: int = 32, shuffle: bool = True, num_workers: int = 2) -> Tuple[DataLoader, Dataset]:
        """
        Returns a PyTorch DataLoader and the underlying Dataset for standard ImageFolder structures.
        """
        dataset = ImageFolder(root=str(self.dataset_path), transform=transform)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
        ai_logger.info(f"Initialized DataLoader with {len(dataset)} samples and {len(dataset.classes)} classes.")
        return dataloader, dataset
