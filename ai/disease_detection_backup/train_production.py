import os
import argparse
import time
import json
import datetime
import numpy as np
import tensorflow as tf
from pathlib import Path
from sklearn.metrics import f1_score
from ai.disease_detection.dataset import load_plantvillage_dataset, compute_class_weights
from ai.disease_detection.model import build_disease_detection_model

def enable_mixed_precision():
    try:
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            policy = tf.keras.mixed_precision.Policy('mixed_float16')
            tf.keras.mixed_precision.set_global_policy(policy)
            print("Mixed precision enabled (mixed_float16).")
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
    except Exception as e:
        print(f"Mixed precision could not be enabled: {e}")

def train_production(data_dir: str, output_dir: str, epochs: int = 2):
    """
    Trains and compares multiple architectures for production.
    Supports resume-capable training.
    """
    enable_mixed_precision()
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    batch_size = 8
    
    print(f"--- Starting PRODUCTION Training ---")
    print(f"Epochs: {epochs}, Batch Size: {batch_size}")
    
    train_ds, val_ds, test_ds, class_names = load_plantvillage_dataset(
        data_dir=data_dir,
        batch_size=batch_size,
        augment=True
    )
    
    class_weights = compute_class_weights(data_dir)
    
    with open(output_path / "class_names.json", "w") as f:
        json.dump(class_names, f)
        
    models_to_train = ["mobilenetv3", "efficientnetb0", "resnet50"]
    registry = {}
    best_model_name = None
    best_score = -1.0 # Combined score based on Val Acc and F1
    
    for model_name in models_to_train:
        print(f"\n======================================")
        print(f" Training {model_name.upper()}")
        print(f"======================================")
        
        model = build_disease_detection_model(
            num_classes=len(class_names),
            model_name=model_name
        )
        
        model_filepath = str(output_path / f"{model_name}_best.keras")
        
        # Resume capability
        if os.path.exists(model_filepath):
            print(f"Found existing weights for {model_name}, loading...")
            try:
                model.load_weights(model_filepath)
            except Exception as e:
                print(f"Failed to load weights: {e}")
        
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', patience=5, restore_best_weights=True
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=model_filepath,
                monitor='val_accuracy', save_best_only=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6
            ),
            tf.keras.callbacks.TensorBoard(log_dir=str(output_path / "logs" / model_name))
        ]
            
        start_time = time.time()
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weights,
            verbose=1
        )
        end_time = time.time()
        
        training_time = end_time - start_time
        
        if not os.path.exists(model_filepath):
            model.save(model_filepath)
            
        print(f"Evaluating {model_name} on validation set for F1 calculation...")
        y_true = []
        y_pred = []
        for x, y in val_ds:
            preds = model.predict(x, verbose=0)
            y_true.extend(np.argmax(y, axis=1))
            y_pred.extend(np.argmax(preds, axis=1))
            
        f1 = float(f1_score(y_true, y_pred, average='weighted'))
        val_acc = float(max(history.history.get("val_accuracy", [0]))) if history.history else float(np.mean(np.array(y_true) == np.array(y_pred)))
        
        # We weigh Val Acc and F1 equally to select the best model
        combined_score = (val_acc + f1) / 2
        print(f"Model: {model_name} | Val Acc: {val_acc:.4f} | F1: {f1:.4f} | Score: {combined_score:.4f}")
        
        if combined_score > best_score:
            best_score = combined_score
            best_model_name = model_name
            
        registry[model_name] = {
            "training_time_seconds": training_time,
            "best_val_accuracy": val_acc,
            "f1_score": f1,
            "combined_score": combined_score
        }
    
    if best_model_name:
        import shutil
        best_model_src = output_path / f"{best_model_name}_best.keras"
        production_model_dst = output_path / "disease_production_best.keras"
        shutil.copy(best_model_src, production_model_dst)
        print(f"\n[INFO] Promoted {best_model_name} to production (Score: {best_score:.4f}).")
    
    metadata = {
        "dataset_source": "PlantVillage (Local Directory)",
        "dataset_version": "1.0",
        "num_classes": len(class_names),
        "training_date": datetime.datetime.now().isoformat(),
        "best_architecture": best_model_name,
        "input_size": [224, 224],
        "evaluation_metrics": registry,
        "model_version": "3.0-production"
    }
        
    with open(output_path / "training_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("\nTraining Phase Complete. Registry updated. Best model exported to production name.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Production Models")
    parser.add_argument("--data_dir", type=str, default="backend/ai_engine/datasets/raw/plantvillage", help="Path to raw dataset")
    parser.add_argument("--output_dir", type=str, default="ai/models/artifacts", help="Output directory")
    parser.add_argument("--epochs", type=int, default=1, help="Number of epochs (1 for validation)")
    args = parser.parse_args()
    
    train_production(args.data_dir, args.output_dir, args.epochs)
