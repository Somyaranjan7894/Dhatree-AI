import os
import json
import joblib
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from ai.crop_recommendation.dataset import get_train_test_split

def evaluate_model():
    model_path = "ai/crop_recommendation/saved_models/best_crop_model.joblib"
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}. Please run train.py first.")
    
    print(f"Loading model from {model_path}...")
    pipeline = joblib.load(model_path)
    
    print("Loading test data...")
    _, X_test, _, y_test = get_train_test_split()
    
    print("Running predictions...")
    y_pred = pipeline.predict(X_test)
    
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc:.4f}")
    
    print("\nClassification Report:")
    report = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    print(classification_report(y_test, y_pred, zero_division=0))
    
    print("Confusion Matrix:")
    labels = sorted(list(set(y_test)))
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print(cm_df)
    
    # Save metrics
    output_dir = "ai/crop_recommendation/saved_models"
    metrics_path = os.path.join(output_dir, "metrics.json")
    
    metrics_data = {
        "accuracy": acc,
        "classification_report": report
    }
    
    with open(metrics_path, 'w') as f:
        json.dump(metrics_data, f, indent=4)
    print(f"\nSaved metrics to {metrics_path}")

if __name__ == "__main__":
    evaluate_model()
