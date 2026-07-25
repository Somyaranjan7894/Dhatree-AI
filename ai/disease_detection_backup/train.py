import os
import argparse
import tensorflow as tf
from pathlib import Path
from ai.disease_detection.dataset import load_plantvillage_dataset
from ai.disease_detection.model import build_disease_detection_model

def train(data_dir: str, output_dir: str, epochs: int = 20, batch_size: int = 32):
    """
    Executes the training loop with callbacks for EarlyStopping and Checkpoints.
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Dataset
    train_ds, val_ds, class_names = load_plantvillage_dataset(
        data_dir=data_dir,
        batch_size=batch_size
    )
    
    # Save class names for inference
    import json
    with open(output_path / "class_names.json", "w") as f:
        json.dump(class_names, f)
        
    # 2. Build Model
    model = build_disease_detection_model(num_classes=len(class_names))
    model.summary()
    
    # 3. Callbacks
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(output_path / "disease_detection_best.keras"),
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            min_lr=1e-6,
            verbose=1
        )
    ]
    
    # 4. Train
    print("Starting training...")
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )
    
    # 5. Save Final Model (in case we want it even if not best)
    model.save(str(output_path / "disease_detection_final.keras"))
    print("Training complete. Models saved.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Disease Detection Model")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to PlantVillage raw dataset")
    parser.add_argument("--output_dir", type=str, default="ai/models/artifacts", help="Path to save models")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch_size", type=int, default=32)
    
    args = parser.parse_args()
    train(args.data_dir, args.output_dir, args.epochs, args.batch_size)
