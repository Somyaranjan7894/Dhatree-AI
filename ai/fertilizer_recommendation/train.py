import os
import json
import time
import logging
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.preprocessing import LabelEncoder

from ai.fertilizer_recommendation.dataset import load_and_validate_dataset
from ai.fertilizer_recommendation.model import get_preprocessor, get_models, build_pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

ARTIFACTS_DIR = Path("ai/models/artifacts")
REGISTRY_PATH = Path("ai/models/fertilizer_training_registry.json")

def evaluate_models():
    """
    Trains multiple models, evaluates them using precision, recall, f1, and speed,
    selects the best, and exports it.
    """
    df = load_and_validate_dataset()
    if df is None or df.empty:
        logging.error("Cannot train models without a valid dataset. Run download_dataset.py first.")
        return

    # Typical columns for fertilizer recommendation dataset:
    # temperature, humidity, rainfall, soil_type, crop_type, nitrogen, potassium, phosphorus, target
    
    # Check if target exists
    if 'target' not in df.columns:
        logging.error("Target column not found in the dataset.")
        return
        
    X = df.drop(columns=['target'])
    y = df['target']
    
    # Encode target labels if XGBoost requires numeric labels or for general safety
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    
    # Identify numeric and categorical columns
    numeric_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_features = X.select_dtypes(include=['object', 'category']).columns.tolist()
    
    preprocessor = get_preprocessor(categorical_features, numeric_features)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded)
    
    models = get_models()
    results = []
    best_f1 = -1
    best_model_name = None
    best_pipeline = None
    
    logging.info(f"Starting training on {len(models)} models...")
    
    for name, clf in models.items():
        logging.info(f"Training {name}...")
        pipeline = build_pipeline(clf, preprocessor)
        
        start_time = time.time()
        pipeline.fit(X_train, y_train)
        train_time = time.time() - start_time
        
        # Inference time
        start_inf = time.time()
        y_pred = pipeline.predict(X_test)
        inf_time = time.time() - start_inf
        
        # Metrics (macro average for multi-class)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='macro', zero_division=0)
        rec = recall_score(y_test, y_pred, average='macro', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='macro', zero_division=0)
        
        # Cross validation (3-fold for speed)
        # We perform CV on the whole X, y to get robust estimate
        cv_scores = cross_val_score(build_pipeline(clf, preprocessor), X, y_encoded, cv=3, scoring='f1_macro')
        cv_mean = cv_scores.mean()
        
        res = {
            "model": name,
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "cv_f1_score": float(cv_mean),
            "training_time_sec": float(train_time),
            "inference_time_sec": float(inf_time)
        }
        results.append(res)
        logging.info(f"{name} metrics: F1={f1:.4f}, CV_F1={cv_mean:.4f}")
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_pipeline = pipeline

    logging.info(f"Best model selected: {best_model_name} with F1: {best_f1:.4f}")
    
    # Save Artifacts
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    
    model_path = ARTIFACTS_DIR / "fertilizer_production_best.joblib"
    encoder_path = ARTIFACTS_DIR / "fertilizer_label_encoder.joblib"
    
    joblib.dump(best_pipeline, model_path)
    joblib.dump(label_encoder, encoder_path)
    
    model_size = os.path.getsize(model_path) / (1024 * 1024)
    logging.info(f"Model saved to {model_path} ({model_size:.2f} MB)")
    
    # Update Registry
    registry = {
        "timestamp": time.time(),
        "selected_model": best_model_name,
        "metrics": next(r for r in results if r["model"] == best_model_name),
        "all_results": results,
        "dataset_rows": len(X),
        "target_classes": list(label_encoder.classes_)
    }
    
    with open(REGISTRY_PATH, "w") as f:
        json.dump(registry, f, indent=4)
        
    logging.info("Training complete and registry updated.")

if __name__ == "__main__":
    evaluate_models()
