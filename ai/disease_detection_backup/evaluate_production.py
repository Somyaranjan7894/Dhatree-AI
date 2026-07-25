import argparse
import json
import os
import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from ai.disease_detection.dataset import load_plantvillage_dataset

def evaluate_production(data_dir: str, output_dir: str):
    """
    Evaluates the best production model on an independent test set.
    """
    output_path = Path(output_dir)
    model_path = output_path / "disease_production_best.keras"
    classes_path = output_path / "class_names.json"
    
    if not model_path.exists():
        raise FileNotFoundError(f"Production model not found at {model_path}")
        
    print(f"Loading production model from {model_path}")
    model = tf.keras.models.load_model(str(model_path))
    
    with open(classes_path, "r") as f:
        class_names = json.load(f)
        
    # Load dataset to get the test split
    print("Loading test dataset...")
    # augment=False for evaluation
    _, _, test_ds, loaded_class_names = load_plantvillage_dataset(
        data_dir=data_dir,
        batch_size=8,
        augment=False
    )
    
    # We must ensure order is deterministic for evaluation
    # test_ds is cached and prefetched, not shuffled in dataset.py
    y_true = []
    y_pred = []
    y_pred_probs = []
    
    print("Running inference on test set...")
    for x, y in test_ds:
        preds = model.predict(x, verbose=0)
        y_true.extend(np.argmax(y, axis=1))
        y_pred.extend(np.argmax(preds, axis=1))
        y_pred_probs.extend(preds)
        
    # Top-3 Accuracy
    top3_correct = 0
    for i in range(len(y_true)):
        top3_classes = np.argsort(y_pred_probs[i])[-3:]
        if y_true[i] in top3_classes:
            top3_correct += 1
    top3_accuracy = top3_correct / len(y_true)
    
    print("\n--- Final Evaluation Metrics ---")
    print(f"Top-1 Accuracy: {np.mean(np.array(y_true) == np.array(y_pred)):.4f}")
    print(f"Top-3 Accuracy: {top3_accuracy:.4f}")
    
    report = classification_report(y_true, y_pred, labels=np.arange(len(class_names)), target_names=class_names, output_dict=True, zero_division=0)
    print("\nClassification Report Generated.")
    
    # Save the classification report
    with open(output_path / "classification_report.json", "w") as f:
        json.dump(report, f, indent=4)
        
    # Identify poorly performing classes (F1 < 0.70)
    poor_classes = {cls: metrics for cls, metrics in report.items() if isinstance(metrics, dict) and metrics.get('f1-score', 1.0) < 0.70 and cls not in ['accuracy', 'macro avg', 'weighted avg']}
    
    if poor_classes:
        print("\n[WARNING] The following classes performed poorly (F1 < 0.70):")
        for cls, metrics in poor_classes.items():
            print(f"  - {cls}: F1 {metrics['f1-score']:.2f}")
    
    # Generate Confusion Matrix
    cm = confusion_matrix(y_true, y_pred, labels=np.arange(len(class_names)))
    plt.figure(figsize=(20, 16))
    sns.heatmap(cm, annot=False, cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title('Confusion Matrix - PlantVillage Disease Detection')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_path / "confusion_matrix.png")
    plt.close()
    
    print(f"\nEvaluation artifacts saved to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate Production Model")
    parser.add_argument("--data_dir", type=str, default="backend/ai_engine/datasets/raw/plantvillage", help="Path to raw dataset")
    parser.add_argument("--output_dir", type=str, default="ai/models/artifacts", help="Output directory")
    args = parser.parse_args()
    
    evaluate_production(args.data_dir, args.output_dir)
