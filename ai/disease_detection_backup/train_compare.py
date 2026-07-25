import os
import argparse
import time
import json
import tensorflow as tf
from pathlib import Path
from ai.disease_detection.dataset import load_plantvillage_dataset
from ai.disease_detection.model import build_disease_detection_model

# Force memory growth to avoid OOM on GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print(f"Detected {len(gpus)} GPU(s). Memory growth enabled.")
    except RuntimeError as e:
        print(e)
else:
    print("No GPU detected. Falling back to CPU.")

def train_models(data_dir: str, output_dir: str, mode: str = "light"):
    """
    Trains and compares multiple architectures.
    mode: 'light' (CPU validation, 1 epoch) or 'production' (Full training)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    epochs = 1 if mode == "light" else 30
    batch_size = 8 if mode == "light" else 32
    
    print(f"--- Starting in {mode.upper()} mode ---")
    print(f"Epochs: {epochs}, Batch Size: {batch_size}")
    
    train_ds, val_ds, class_names = load_plantvillage_dataset(
        data_dir=data_dir,
        batch_size=batch_size,
        augment=(mode == "production")
    )
    
    with open(output_path / "class_names.json", "w") as f:
        json.dump(class_names, f)
        
    models_to_train = ["mobilenetv3", "efficientnetb0", "resnet50"]
    registry = {}
    
    for model_name in models_to_train:
        print(f"\n======================================")
        print(f" Training {model_name.upper()}")
        print(f"======================================")
        
        model = build_disease_detection_model(
            num_classes=len(class_names),
            model_name=model_name
        )
        
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor='val_loss', patience=5, restore_best_weights=True
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=str(output_path / f"{model_name}_best.keras"),
                monitor='val_accuracy', save_best_only=True
            )
        ]
        
        # Add TensorBoard logging for production
        if mode == "production":
            tb_dir = output_path / "logs" / model_name
            callbacks.append(tf.keras.callbacks.TensorBoard(log_dir=str(tb_dir)))
            callbacks.append(tf.keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6
            ))
            
        start_time = time.time()
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks,
            verbose=1
        )
        end_time = time.time()
        
        training_time = end_time - start_time
        
        registry[model_name] = {
            "training_time_seconds": training_time,
            "best_val_accuracy": float(max(history.history.get("val_accuracy", [0]))),
            "best_val_loss": float(min(history.history.get("val_loss", [0])))
        }
        
    with open(output_path / "training_registry.json", "w") as f:
        json.dump(registry, f, indent=4)
        
    print("\nTraining Phase Complete. Registry updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train and Compare Models")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to raw dataset")
    parser.add_argument("--output_dir", type=str, default="ai/models/artifacts", help="Output directory")
    parser.add_argument("--mode", type=str, choices=["light", "production"], default="light", help="Training mode")
    args = parser.parse_args()
    
    train_models(args.data_dir, args.output_dir, args.mode)
