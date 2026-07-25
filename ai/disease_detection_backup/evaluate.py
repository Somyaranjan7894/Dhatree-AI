import argparse
import json
import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
from ai.disease_detection.dataset import load_plantvillage_dataset

def evaluate_model(model_path: str, data_dir: str, batch_size: int = 32):
    """
    Evaluates the trained model against the validation split and computes scikit-learn metrics.
    """
    path = Path(model_path)
    if not path.exists():
        raise FileNotFoundError(f"Model not found at {path}")
        
    print(f"Loading model from {path}...")
    model = tf.keras.models.load_model(path)
    
    print("Loading validation dataset...")
    # Using the same seed guarantees the same split
    _, val_ds, class_names = load_plantvillage_dataset(data_dir=data_dir, batch_size=batch_size)
    
    print("Running inference on validation set...")
    y_true = []
    y_pred = []
    
    for images, labels in val_ds:
        preds = model.predict(images, verbose=0)
        y_pred.extend(np.argmax(preds, axis=1))
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        
    print("Calculating metrics...")
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    rec = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    
    cm = confusion_matrix(y_true, y_pred)
    report = classification_report(y_true, y_pred, target_names=class_names, zero_division=0)
    
    metrics = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "confusion_matrix": cm.tolist()
    }
    
    print(f"\nAccuracy: {acc:.4f} | F1 Score: {f1:.4f}")
    print("\nClassification Report:")
    print(report)
    
    # Save metrics
    output_meta = path.parent / f"{path.stem}_eval.json"
    with open(output_meta, 'w') as f:
        json.dump(metrics, f, indent=4)
    print(f"Metrics saved to {output_meta}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Disease Detection Model")
    parser.add_argument("--model_path", type=str, required=True, help="Path to .keras model file")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to PlantVillage raw dataset")
    parser.add_argument("--batch_size", type=int, default=32)
    
    args = parser.parse_args()
    evaluate_model(args.model_path, args.data_dir, args.batch_size)
