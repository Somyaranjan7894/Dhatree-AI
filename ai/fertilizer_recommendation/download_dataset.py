import os
import json
import logging
from pathlib import Path
import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Usually gdhasija/fertilizer-recommendation is a good one
DATASET_OWNER = "gdhasija"
DATASET_NAME = "fertilizer-recommendation"
RAW_DATA_DIR = Path("ai/datasets/raw/fertilizer")
METADATA_DIR = Path("ai/datasets/metadata/fertilizer")

def check_kaggle_credentials():
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        logging.warning("Kaggle credentials not found!")
        logging.warning("Please create an account on Kaggle, go to your profile settings, and click 'Create New API Token'.")
        logging.warning(f"Place the downloaded 'kaggle.json' file in {kaggle_dir} and ensure proper permissions.")
        return False
    return True

def download_and_extract():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if list(RAW_DATA_DIR.glob("*.csv")):
        logging.info("Dataset directory is not empty. Assuming dataset is already downloaded.")
        return
        
    if not check_kaggle_credentials():
        logging.error("Missing Kaggle credentials. Pipeline requires actual dataset. Please configure Kaggle and re-run.")
        logging.info("Setup Instructions: \n1. Get kaggle.json from Kaggle Profile.\n2. Place in ~/.kaggle/\n3. Re-run this script.")
        # We don't generate dummy data as per instructions.
        return
        
    logging.info(f"Downloading {DATASET_OWNER}/{DATASET_NAME} using Kaggle API...")
    
    try:
        import kaggle
        kaggle.api.authenticate()
        kaggle.api.dataset_download_files(f"{DATASET_OWNER}/{DATASET_NAME}", path=str(RAW_DATA_DIR), unzip=True)
        logging.info("Download and extraction complete.")
        
        # Save versioning metadata
        metadata = {
            "dataset": f"{DATASET_OWNER}/{DATASET_NAME}",
            "downloaded_at": datetime.datetime.now().isoformat(),
            "version": "1.0",
            "source": "kaggle"
        }
        with open(METADATA_DIR / "dataset_version.json", "w") as f:
            json.dump(metadata, f, indent=4)
            
    except Exception as e:
        logging.error(f"Failed to download dataset via Kaggle API: {e}")
        logging.info("Please manually download the dataset and extract the CSV to 'ai/datasets/raw/fertilizer'")

if __name__ == "__main__":
    download_and_extract()
