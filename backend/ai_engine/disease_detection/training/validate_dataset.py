import os
import sys
import hashlib
from pathlib import Path
from PIL import Image

def validate_plantvillage_dataset(dataset_dir: str):
    print(f"Starting Dataset Validation for {dataset_dir}...")
    dataset_path = Path(dataset_dir)
    
    if not dataset_path.exists() or not dataset_path.is_dir():
        print(f"Error: Dataset directory does not exist: {dataset_dir}")
        sys.exit(1)
        
    classes = [d for d in os.listdir(dataset_path) if (dataset_path / d).is_dir()]
    num_classes = len(classes)
    
    print(f"Detected Classes: {num_classes}")
    
    if num_classes == 0:
        print("Error: No classes detected.")
        sys.exit(1)
        
    supported_formats = {'.jpg', '.jpeg', '.png'}
    
    total_images = 0
    empty_folders = []
    corrupted_images = []
    unsupported_images = []
    
    image_hashes = {}
    duplicate_images = []
    
    class_counts = {}
    
    for class_name in classes:
        class_dir = dataset_path / class_name
        files = [f for f in os.listdir(class_dir) if (class_dir / f).is_file()]
        
        if not files:
            empty_folders.append(class_name)
            continue
            
        class_img_count = 0
        for f in files:
            file_path = class_dir / f
            ext = file_path.suffix.lower()
            
            if ext not in supported_formats:
                unsupported_images.append(str(file_path))
                continue
                
            try:
                with Image.open(file_path) as img:
                    img.verify()
                    
                # Compute hash for duplicates
                with open(file_path, "rb") as image_file:
                    file_hash = hashlib.md5(image_file.read()).hexdigest()
                    if file_hash in image_hashes:
                        duplicate_images.append((str(file_path), image_hashes[file_hash]))
                    else:
                        image_hashes[file_hash] = str(file_path)
                        
                class_img_count += 1
                total_images += 1
            except Exception as e:
                corrupted_images.append(str(file_path))
                
        class_counts[class_name] = class_img_count
        print(f"  - {class_name}: {class_img_count} images")

    print("\n--- Validation Report ---")
    print(f"Total Classes: {num_classes}")
    print(f"Total Valid Images: {total_images}")
    
    issues_found = False
    
    if empty_folders:
        print(f"[FAILED] Empty Folders Detected ({len(empty_folders)}): {empty_folders}")
        issues_found = True
    else:
        print("[OK] No empty folders.")
        
    if unsupported_images:
        print(f"[FAILED] Unsupported Images ({len(unsupported_images)} found). Example: {unsupported_images[:3]}")
        issues_found = True
    else:
        print("[OK] All images have supported formats.")
        
    if corrupted_images:
        print(f"[FAILED] Corrupted Images ({len(corrupted_images)} found). Example: {corrupted_images[:3]}")
        issues_found = True
    else:
        print("[OK] No corrupted images.")
        
    if duplicate_images:
        print(f"[FAILED] Duplicate Images ({len(duplicate_images)} found). Example: {duplicate_images[:3]}")
        issues_found = True
    else:
        print("[OK] No duplicate images.")
        
    if issues_found:
        print("\nDataset validation FAILED. Fix issues before training.")
        sys.exit(1)
    else:
        print("\nDataset validation PASSED. Ready for training.")
        sys.exit(0)

if __name__ == "__main__":
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    dataset_loc = BASE_DIR / "ai_engine" / "datasets" / "raw" / "plantvillage"
    validate_plantvillage_dataset(str(dataset_loc))
