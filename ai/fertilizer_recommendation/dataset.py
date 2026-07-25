import os
import json
import logging
import pandas as pd
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

RAW_DATA_DIR = Path("ai/datasets/raw/fertilizer")
METADATA_DIR = Path("ai/datasets/metadata/fertilizer")
REPORT_PATH = METADATA_DIR / "validation_report.json"

def load_and_validate_dataset():
    """
    Loads the fertilizer dataset, handles missing/duplicate values, and validates the schema.
    """
    if not RAW_DATA_DIR.exists():
        logging.error(f"Dataset directory not found: {RAW_DATA_DIR}")
        return None
        
    csv_files = list(RAW_DATA_DIR.glob("*.csv"))
    if not csv_files:
        logging.error("No CSV files found in dataset directory.")
        return None
        
    # Assume the first CSV is our dataset
    df = pd.read_csv(csv_files[0])
    
    report = {
        "initial_rows": int(len(df)),
        "columns": list(df.columns),
        "issues": []
    }
    
    # Standardize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    
    # Rename commonly differing columns to standard format
    # The dataset usually has: Temparature, Humidity, Moisture, Soil Type, Crop Type, Nitrogen, Potassium, Phosphorous, Fertilizer Name
    rename_map = {
        'temparature': 'temperature',
        'moisture': 'rainfall',  # Often moisture is a proxy in fertilizer dataset, let's keep it aligned with our schema
        'phosphorous': 'phosphorus',
        'fertilizer_name': 'target'
    }
    df.rename(columns=rename_map, inplace=True)
    
    required_cols = ['temperature', 'humidity', 'nitrogen', 'potassium', 'phosphorus', 'soil_type', 'crop_type', 'target']
    
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        report["issues"].append(f"Missing required columns: {missing_cols}")
        logging.error(f"Missing required columns: {missing_cols}")
        # Proceed with what we have, but it might fail
        
    # Handle duplicates
    duplicates = int(df.duplicated().sum())
    if duplicates > 0:
        report["issues"].append(f"Found {duplicates} duplicate rows.")
        df.drop_duplicates(inplace=True)
        
    # Handle missing values
    missing_vals = df.isnull().sum().to_dict()
    missing_vals = {k: int(v) for k, v in missing_vals.items() if v > 0}
    if missing_vals:
        report["issues"].append(f"Found missing values: {missing_vals}")
        df.dropna(inplace=True)
        
    report["final_rows"] = int(len(df))
    
    if 'target' in df.columns:
        report["classes"] = df['target'].value_counts().to_dict()
        
    METADATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, indent=4)
        
    logging.info(f"Dataset validated. Final shape: {df.shape}")
    
    return df

if __name__ == "__main__":
    load_and_validate_dataset()
