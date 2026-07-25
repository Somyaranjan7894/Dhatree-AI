import argparse
import datetime
import json
import os
import shutil

# Add backend to sys.path if running standalone to resolve imports correctly
import sys
import time
from pathlib import Path

import numpy as np
import tensorflow as tf
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from ai_engine.disease_detection.utils.dataset_utils import (
    compute_class_weights,
    load_plantvillage_dataset,
)
from ai_engine.disease_detection.utils.model_utils import build_disease_detection_model


def enable_mixed_precision():
    try:
        gpus = tf.config.list_physical_devices("GPU")
        if gpus:
            policy = tf.keras.mixed_precision.Policy("mixed_float16")
            tf.keras.mixed_precision.set_global_policy(policy)
            print("Mixed precision enabled (mixed_float16).")
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
    except Exception as e:
        print(f"Mixed precision could not be enabled: {e}")


def train_production(epochs: int = 2, batch_size: int = 8):
    enable_mixed_precision()

    current_dir = Path(__file__).resolve().parent
    base_module_dir = current_dir.parent

    data_dir = base_module_dir / "datasets" / "raw" / "plantvillage"
    checkpoints_dir = base_module_dir / "models" / "checkpoints"
    logs_dir = base_module_dir / "models" / "logs"

    # Destination for the best model to match ModelsRegistry
    registry_export_dir = base_module_dir.parent / "models" / "disease_detection"
    registry_export_dir.mkdir(parents=True, exist_ok=True)
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    logs_dir.mkdir(parents=True, exist_ok=True)

    print(f"--- Starting PRODUCTION Training ---")
    print(f"Dataset path: {data_dir}")
    print(f"Epochs: {epochs}, Batch Size: {batch_size}")

    train_ds, val_ds, test_ds, class_names = load_plantvillage_dataset(
        data_dir=str(data_dir), batch_size=batch_size, augment=True
    )

    class_weights = compute_class_weights(str(data_dir))

    # Export class names right away
    with open(registry_export_dir / "class_names.json", "w") as f:
        json.dump(class_names, f)

    models_to_train = ["mobilenetv3", "efficientnetb0", "resnet50"]
    registry = {}
    best_model_name = None
    best_score = -1.0

    for model_name in models_to_train:
        print(f"\n======================================")
        print(f" Training {model_name.upper()}")
        print(f"======================================")

        model = build_disease_detection_model(
            num_classes=len(class_names), model_name=model_name
        )

        model_filepath = str(checkpoints_dir / f"{model_name}_best.keras")

        if os.path.exists(model_filepath):
            print(f"Found existing weights for {model_name}, loading...")
            try:
                model.load_weights(model_filepath)
            except Exception as e:
                print(f"Failed to load weights: {e}")

        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=5, restore_best_weights=True
            ),
            tf.keras.callbacks.ModelCheckpoint(
                filepath=model_filepath, monitor="val_accuracy", save_best_only=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.2, patience=3, min_lr=1e-6
            ),
            tf.keras.callbacks.TensorBoard(log_dir=str(logs_dir / model_name)),
        ]

        start_time = time.time()
        history = model.fit(
            train_ds,
            validation_data=val_ds,
            epochs=epochs,
            callbacks=callbacks,
            class_weight=class_weights,
            verbose=1,
        )
        end_time = time.time()
        training_time = end_time - start_time

        if not os.path.exists(model_filepath):
            model.save(model_filepath)

        print(f"Evaluating {model_name} on test set for metrics...")
        y_true = []
        y_pred = []
        y_scores = []
        for x, y in test_ds:
            preds = model.predict(x, verbose=0)
            y_true.extend(np.argmax(y, axis=1))
            y_pred.extend(np.argmax(preds, axis=1))
            y_scores.extend(preds)

        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        y_scores = np.array(y_scores)

        f1 = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
        precision = float(
            precision_score(y_true, y_pred, average="weighted", zero_division=0)
        )
        recall = float(
            recall_score(y_true, y_pred, average="weighted", zero_division=0)
        )

        top1_acc = float(np.mean(y_true == y_pred))

        # Calculate Top-3 Accuracy
        top3_preds = np.argsort(y_scores, axis=1)[:, -3:]
        top3_acc = float(
            np.mean([y_true[i] in top3_preds[i] for i in range(len(y_true))])
        )

        print(f"\nClassification Report for {model_name}:")
        print(
            classification_report(
                y_true, y_pred, target_names=class_names, zero_division=0
            )
        )

        print(f"\nConfusion Matrix for {model_name}:")
        print(confusion_matrix(y_true, y_pred))

        # Per-class accuracy
        cm = confusion_matrix(y_true, y_pred)
        per_class_acc = cm.diagonal() / np.maximum(cm.sum(axis=1), 1)
        poor_classes = [
            class_names[i] for i, acc in enumerate(per_class_acc) if acc < 0.5
        ]
        if poor_classes:
            print(f"Classes with poor performance (<50%): {poor_classes}")

        combined_score = (top1_acc + f1) / 2
        print(
            f"Model: {model_name} | Top-1 Acc: {top1_acc:.4f} | Top-3 Acc: {top3_acc:.4f} | F1: {f1:.4f} | Precision: {precision:.4f} | Recall: {recall:.4f}"
        )

        if combined_score > best_score:
            best_score = combined_score
            best_model_name = model_name

        registry[model_name] = {
            "training_time_seconds": training_time,
            "test_accuracy": top1_acc,
            "top3_accuracy": top3_acc,
            "precision": precision,
            "recall": recall,
            "f1_score": f1,
            "combined_score": combined_score,
            "poor_performing_classes": poor_classes,
        }

    if best_model_name:
        best_model_src = checkpoints_dir / f"{best_model_name}_best.keras"
        production_model_dst = registry_export_dir / "disease_production_best.keras"
        shutil.copy(best_model_src, production_model_dst)
        print(
            f"\n[INFO] Promoted {best_model_name} to production (Score: {best_score:.4f})."
        )

    metadata = {
        "dataset_source": "PlantVillage",
        "dataset_path": str(data_dir),
        "dataset_version": "1.0",
        "num_classes": len(class_names),
        "total_images": sum([len(files) for r, d, files in os.walk(data_dir)]),
        "split": "70/15/15",
        "training_date": datetime.datetime.now().isoformat(),
        "best_architecture": best_model_name,
        "epochs": epochs,
        "input_size": [224, 224],
        "evaluation_metrics": registry,
        "best_model_metrics": registry.get(best_model_name, {}),
        "model_version": "3.0-production",
    }

    with open(registry_export_dir / "training_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)

    print("\nTraining Phase Complete. Registry updated. Best model exported.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Production Models")
    parser.add_argument("--epochs", type=int, default=2, help="Number of epochs")
    parser.add_argument("--batch_size", type=int, default=8, help="Batch size")
    args = parser.parse_args()

    train_production(args.epochs, args.batch_size)
