import os
import argparse
import json
import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

import sys
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from ai_engine.disease_detection.utils.dataset_utils import load_plantvillage_dataset

def evaluate_production():
    current_dir = Path(__file__).resolve().parent
    base_module_dir = current_dir.parent
    
    data_dir = base_module_dir / "datasets" / "raw" / "plantvillage"
    models_registry_dir = base_module_dir.parent / "models" / "disease_detection"
    
    model_path = models_registry_dir / "disease_production_best.keras"
    classes_path = models_registry_dir / "class_names.json"
    
    if not model_path.exists():
        raise FileNotFoundError(f"Production model not found at {model_path}")
        
    print(f"Loading production model from {model_path}")
    model = tf.keras.models.load_model(str(model_path))
    
    with open(classes_path, "r") as f:
        class_names = json.load(f)
        
    print("Loading test dataset...")
    _, _, test_ds, loaded_class_names = load_plantvillage_dataset(
        data_dir=str(data_dir),
        batch_size=8,
        augment=False
    )
    
    y_true = []
    y_pred = []
    y_pred_probs = []
    
    print("Running inference on test set...")
    for x, y in test_ds:
        preds = model.predict(x, verbose=0)
        y_true.extend(np.argmax(y, axis=1))
        y_pred.extend(np.argmax(preds, axis=1))
        y_pred_probs.extend(preds)
        
    top3_correct = 0
    for i in range(len(y_true)):
        top3_classes = np.argsort(y_pred_probs[i])[-3:]
        if y_true[i] in top3_classes:
            top3_correct += 1
    top3_accuracy = top3_correct / len(y_true)
    
    top1_accuracy = np.mean(np.array(y_true) == np.array(y_pred))
    
    print("\n--- Final Evaluation Metrics ---")
    print(f"Top-1 Accuracy: {top1_accuracy:.4f}")
    print(f"Top-3 Accuracy: {top3_accuracy:.4f}")
    
    report = classification_report(y_true, y_pred, labels=np.arange(len(class_names)), target_names=class_names, output_dict=True, zero_division=0)
    print("\nClassification Report Generated.")
    
    with open(current_dir / "classification_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    poor_classes = {cls: metrics for cls, metrics in report.items() if isinstance(metrics, dict) and metrics.get('f1-score', 1.0) < 0.70 and cls not in ['accuracy', 'macro avg', 'weighted avg']}
    
    if poor_classes:
        print("\n[WARNING] The following classes performed poorly (F1 < 0.70):")
        for cls, metrics in poor_classes.items():
            print(f"  - {cls}: F1 {metrics['f1-score']:.2f}")
    
    cm = confusion_matrix(y_true, y_pred, labels=np.arange(len(class_names)))
    plt.figure(figsize=(20, 16))
    sns.heatmap(cm, annot=False, cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix - PlantVillage Disease Detection')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(current_dir / "confusion_matrix.png")
    plt.close()
    
    print(f"\nEvaluation artifacts saved to {current_dir}")

if __name__ == "__main__":
    evaluate_production()
