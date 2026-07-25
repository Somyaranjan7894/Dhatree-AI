import os
import argparse
import json
import time
from pathlib import Path
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report
import numpy as np

def evaluate_models(data_dir: str, artifacts_dir: str):
    """
    Evaluates all trained models in artifacts_dir and selects the best one.
    """
    artifacts_path = Path(artifacts_dir)
    data_path = Path(data_dir)
    
    # Load test dataset
    print(f"Loading test dataset from: {data_path}")
    test_ds = tf.keras.utils.image_dataset_from_directory(
        data_path,
        validation_split=0.1,  # Use 10% as a mock test set if we don't have a dedicated one
        subset="validation",
        seed=42,
        image_size=(224, 224),
        batch_size=32,
        label_mode='categorical'
    )
    
    # Get true labels
    y_true = []
    for _, labels in test_ds.unbatch():
        y_true.append(np.argmax(labels.numpy()))
    y_true = np.array(y_true)
    
    # Get class names
    with open(artifacts_path / "class_names.json", "r") as f:
        class_names = json.load(f)
        
    models_to_evaluate = ["mobilenetv3", "efficientnetb0", "resnet50"]
    results = {}
    
    for model_name in models_to_evaluate:
        model_path = artifacts_path / f"{model_name}_best.keras"
        if not model_path.exists():
            print(f"Skipping {model_name}: Model file not found at {model_path}")
            continue
            
        print(f"\nEvaluating {model_name}...")
        model = tf.keras.models.load_model(str(model_path))
        
        # Calculate model size in MB
        model_size_mb = os.path.getsize(model_path) / (1024 * 1024)
        
        # Inference speed
        start_time = time.time()
        y_pred_probs = model.predict(test_ds, verbose=0)
        end_time = time.time()
        
        inference_time_ms_per_image = ((end_time - start_time) / len(y_true)) * 1000
        
        y_pred = np.argmax(y_pred_probs, axis=1)
        
        # Metrics
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        # Validation Loss
        loss, _ = model.evaluate(test_ds, verbose=0)
        
        results[model_name] = {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "val_loss": float(loss),
            "inference_time_ms": float(inference_time_ms_per_image),
            "model_size_mb": float(model_size_mb)
        }
        
    if not results:
        print("No models evaluated.")
        return
        
    # Select best model using a custom score: high F1, low loss, low inference time, low size
    # For simplicity, let's heavily weight F1 score and val_loss
    best_model_name = None
    best_score = -float('inf')
    
    for m, metrics in results.items():
        # A simple scoring function
        score = (metrics["f1_score"] * 100) - (metrics["val_loss"] * 10) - (metrics["inference_time_ms"] / 10)
        if score > best_score:
            best_score = score
            best_model_name = m
            
    print(f"\n======================================")
    print(f" Best Model Selected: {best_model_name.upper()} (Score: {best_score:.2f})")
    print(f"======================================")
    
    # Save comparison report
    report = {
        "best_model": best_model_name,
        "metrics": results
    }
    
    reports_dir = Path("ai/datasets/reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    with open(reports_dir / "model_comparison.json", "w") as f:
        json.dump(report, f, indent=4)
        
    # Copy best model to production location
    import shutil
    src_model = artifacts_path / f"{best_model_name}_best.keras"
    dst_model = artifacts_path / "disease_production_best.keras"
    shutil.copy2(src_model, dst_model)
    print(f"Production model saved to {dst_model}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate and Select Best Model")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to raw dataset")
    parser.add_argument("--artifacts_dir", type=str, default="ai/models/artifacts", help="Model artifacts directory")
    args = parser.parse_args()
    
    evaluate_models(args.data_dir, args.artifacts_dir)
