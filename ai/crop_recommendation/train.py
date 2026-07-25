import os
import time
import joblib
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from ai.crop_recommendation.dataset import get_train_test_split
from ai.crop_recommendation.model import MODELS

def train_and_evaluate():
    print("Loading dataset...")
    X_train, X_test, y_train, y_test = get_train_test_split()
    print(f"Train size: {X_train.shape[0]}, Test size: {X_test.shape[0]}")
    
    results = []
    best_model_name = None
    best_model_pipeline = None
    best_f1 = -1
    
    print("\nComparing Models...")
    for name, get_pipeline in MODELS.items():
        print(f"\n--- Training {name} ---")
        pipeline = get_pipeline()
        
        # 1. Cross Validation
        cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring='f1_weighted')
        print(f"CV F1 (Weighted) Mean: {cv_scores.mean():.4f}")
        
        # 2. Training Time
        start_time = time.time()
        pipeline.fit(X_train, y_train)
        training_time = time.time() - start_time
        print(f"Training Time: {training_time:.4f} seconds")
        
        # 3. Evaluation on Test Set
        y_pred = pipeline.predict(X_test)
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
        print(f"F1 Score:  {f1:.4f}")
        
        results.append({
            'Model': name,
            'CV_F1': cv_scores.mean(),
            'Train_Time': training_time,
            'Accuracy': acc,
            'Precision': prec,
            'Recall': rec,
            'F1_Score': f1
        })
        
        if f1 > best_f1:
            best_f1 = f1
            best_model_name = name
            best_model_pipeline = pipeline

    print("\n==============================")
    print("Model Comparison Summary:")
    print(pd.DataFrame(results))
    print("==============================\n")
    
    print(f"Selected Best Model: {best_model_name} with F1 Score: {best_f1:.4f}")
    
    # Save the best model
    output_dir = "ai/crop_recommendation/saved_models"
    os.makedirs(output_dir, exist_ok=True)
    model_path = os.path.join(output_dir, "best_crop_model.joblib")
    
    joblib.dump(best_model_pipeline, model_path)
    print(f"Saved complete inference pipeline to {model_path}")

if __name__ == "__main__":
    train_and_evaluate()
