import pandas as pd
import os
from sklearn.model_selection import train_test_split

def load_data(csv_path="ai/datasets/raw/crop_recommendation/crop_recommendation.csv"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}")
    
    df = pd.read_csv(csv_path)
    
    # Check for required columns
    required_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
            
    # Handle missing values (if any)
    # For numeric columns, fill with median
    numeric_cols = ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    # For label, drop missing
    df = df.dropna(subset=['label'])
    
    X = df[numeric_cols]
    y = df['label']
    
    return X, y

def get_train_test_split(test_size=0.2, random_state=42):
    X, y = load_data()
    return train_test_split(X, y, test_size=test_size, random_state=random_state)
