import json
import logging
import os
from pathlib import Path

from PIL import Image

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)

# Dynamic paths based on current file location
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "datasets" / "raw" / "plantvillage"
PROCESSED_DIR = BASE_DIR / "datasets" / "processed"
REPORT_PATH = PROCESSED_DIR / "validation_report.json"


def validate_dataset():
    if not RAW_DATA_DIR.exists():
        logging.error(f"Dataset directory not found: {RAW_DATA_DIR}")
        return

    report = {
        "total_images": 0,
        "classes": {},
        "corrupted_images": [],
        "empty_classes": [],
        "issues": [],
    }

    # We expect PlantVillage dataset might have a subfolder like 'PlantVillage' or just the class folders
    subdirs = [d for d in RAW_DATA_DIR.iterdir() if d.is_dir()]
    if len(subdirs) == 1 and subdirs[0].name == "PlantVillage":
        base_dir = subdirs[0]
    elif any(d.name.startswith("PlantVillage-") for d in subdirs):
        # Handle 'PlantVillage-Dataset' style wrappers
        base_dir = next(d for d in subdirs if d.name.startswith("PlantVillage-"))
        base_dir = (
            base_dir / "raw" / "color"
            if (base_dir / "raw" / "color").exists()
            else base_dir
        )
    else:
        base_dir = RAW_DATA_DIR

    class_folders = [d for d in base_dir.iterdir() if d.is_dir()]

    if not class_folders:
        report["issues"].append("No class directories found.")
        logging.error("No class directories found.")

    for cls_folder in class_folders:
        class_name = cls_folder.name
        images = list(cls_folder.glob("*.*"))

        if not images:
            report["empty_classes"].append(class_name)
            continue

        valid_images_count = 0
        for img_path in images:
            if img_path.suffix.lower() not in [".jpg", ".jpeg", ".png"]:
                continue

            try:
                with Image.open(img_path) as img:
                    img.verify()  # Check if it's a valid image
                valid_images_count += 1
            except Exception as e:
                report["corrupted_images"].append(str(img_path))

        report["classes"][class_name] = valid_images_count
        report["total_images"] += valid_images_count

    # Check class imbalance
    if report["classes"]:
        counts = list(report["classes"].values())
        max_count = max(counts)
        min_count = min(counts)
        if max_count > min_count * 10:
            report["issues"].append(
                "Severe class imbalance detected (>10x difference between max and min class)"
            )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)

    logging.info(
        f"Validation complete. Found {report['total_images']} valid images across {len(report['classes'])} classes."
    )
    logging.info(f"Found {len(report['corrupted_images'])} corrupted images.")
    if report["issues"]:
        logging.warning(f"Issues detected: {report['issues']}")
    logging.info(f"Report saved to: {REPORT_PATH}")


if __name__ == "__main__":
    validate_dataset()
