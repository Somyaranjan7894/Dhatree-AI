import os
import sys
import hashlib
from pathlib import Path
from collections import defaultdict

def deduplicate_dataset(dataset_dir: str):
    dataset_path = Path(dataset_dir)
    print(f"Starting Dataset Deduplication for {dataset_path}...")
    
    classes = sorted([d for d in os.listdir(dataset_path) if (dataset_path / d).is_dir()])
    
    hash_to_files = defaultdict(list)
    
    for class_name in classes:
        class_dir = dataset_path / class_name
        files = [f for f in os.listdir(class_dir) if (class_dir / f).is_file()]
        
        for f in files:
            file_path = class_dir / f
            ext = file_path.suffix.lower()
            if ext not in {'.jpg', '.jpeg', '.png'}:
                continue
                
            try:
                with open(file_path, "rb") as fp:
                    file_hash = hashlib.md5(fp.read()).hexdigest()
                hash_to_files[file_hash].append((class_name, str(file_path)))
            except Exception as e:
                print(f"Error reading {file_path}: {e}")
                
    # Now analyze duplicates
    cross_class_duplicates = []
    removed_count = 0
    
    print("\n--- Deletion Report ---")
    for file_hash, file_list in hash_to_files.items():
        if len(file_list) > 1:
            classes_in_group = set([item[0] for item in file_list])
            if len(classes_in_group) > 1:
                cross_class_duplicates.append(file_list)
            else:
                original = file_list[0]
                duplicates = file_list[1:]
                print(f"Hash: {file_hash}")
                print(f"  Class: {original[0]}")
                print(f"  Retained: {original[1]}")
                for dup in duplicates:
                    print(f"  Removed: {dup[1]}")
                    os.remove(dup[1])
                    removed_count += 1
                    
    print("\n--- Summary ---")
    print(f"Total redundant duplicates removed: {removed_count}")
    
    if cross_class_duplicates:
        print("\nWARNING: Found duplicates across different classes. They were NOT deleted automatically.")
        for group in cross_class_duplicates:
            print("Group:")
            for item in group:
                print(f"  Class: {item[0]} | Path: {item[1]}")
        sys.exit(2)
        
    print("Deduplication complete.")
    
if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    dataset_dir = base_dir / "ai" / "datasets" / "raw" / "plantvillage"
    deduplicate_dataset(str(dataset_dir))
