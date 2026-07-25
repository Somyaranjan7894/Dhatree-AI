import os
import sys
import json
import hashlib
import time
import shutil
import datetime
import argparse
from pathlib import Path

import numpy as np
import tensorflow as tf
from PIL import Image
from sklearn.metrics import f1_score, precision_score, recall_score, classification_report, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight

def enable_mixed_precision():
    try:
        gpus = tf.config.list_physical_devices('GPU')
        if gpus:
            policy = tf.keras.mixed_precision.Policy('mixed_float16')
            tf.keras.mixed_precision.set_global_policy(policy)
            print("Mixed precision enabled.")
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
    except Exception as e:
        print(f"Mixed precision not enabled: {e}")

def validate_dataset(dataset_dir: str):
    dataset_path = Path(dataset_dir)
    print(f"Validating dataset at {dataset_path}...")
    
    if not dataset_path.exists():
        print(f"Error: Path {dataset_path} does not exist.")
        sys.exit(1)
        
    classes = sorted([d for d in os.listdir(dataset_path) if (dataset_path / d).is_dir()])
    num_classes = len(classes)
    
    print(f"Detected {num_classes} classes.")
    
    supported_formats = {'.jpg', '.jpeg', '.png'}
    total_images = 0
    empty_folders = []
    corrupted_images = []
    duplicate_images = []
    image_hashes = {}
    
    for class_name in classes:
        class_dir = dataset_path / class_name
        files = [f for f in os.listdir(class_dir) if (class_dir / f).is_file()]
        
        if not files:
            empty_folders.append(class_name)
            continue
            
        for f in files:
            file_path = class_dir / f
            ext = file_path.suffix.lower()
            if ext not in supported_formats:
                continue
            
            try:
                with Image.open(file_path) as img:
                    img.verify()
                
                with open(file_path, "rb") as fp:
                    file_hash = hashlib.md5(fp.read()).hexdigest()
                    if file_hash in image_hashes:
                        duplicate_images.append(str(file_path))
                    else:
                        image_hashes[file_hash] = str(file_path)
                total_images += 1
            except Exception:
                corrupted_images.append(str(file_path))

    print(f"Total valid images: {total_images}")
    if empty_folders or corrupted_images or duplicate_images:
        print(f"Validation FAILED.")
        print(f"Empty folders: {len(empty_folders)}")
        print(f"Corrupted images: {len(corrupted_images)}")
        print(f"Duplicate images: {len(duplicate_images)}")
        if duplicate_images:
            print("List of duplicate images:")
            for d in duplicate_images:
                print(f"  - {d}")
        sys.exit(1)
        
    print("Dataset Validation PASSED.")
    return classes

def get_data_augmentation():
    return tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal"),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.2),
        tf.keras.layers.RandomContrast(0.2),
        tf.keras.layers.RandomBrightness(0.2),
        tf.keras.layers.RandomTranslation(height_factor=0.1, width_factor=0.1)
    ])

def build_model(num_classes, model_name):
    inputs = tf.keras.Input(shape=(224, 224, 3))
    
    if model_name == "mobilenetv3":
        x = tf.keras.applications.mobilenet_v3.preprocess_input(inputs)
        base = tf.keras.applications.MobileNetV3Large(input_shape=(224,224,3), include_top=False, weights='imagenet')
    elif model_name == "efficientnetb0":
        x = tf.keras.applications.efficientnet.preprocess_input(inputs)
        base = tf.keras.applications.EfficientNetB0(input_shape=(224,224,3), include_top=False, weights='imagenet')
    elif model_name == "resnet50":
        x = tf.keras.applications.resnet50.preprocess_input(inputs)
        base = tf.keras.applications.ResNet50(input_shape=(224,224,3), include_top=False, weights='imagenet')
    
    base.trainable = False
    x = base(x, training=False)
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(0.2)(x)
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax')(x)
    
    model = tf.keras.Model(inputs, outputs)
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-4),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    return model

def main():
    enable_mixed_precision()
    
    base_dir = Path(__file__).resolve().parent.parent
    dataset_dir = base_dir / "ai" / "datasets" / "raw" / "plantvillage"
    export_dir = base_dir / "ai" / "models" / "disease_detection"
    
    export_dir.mkdir(parents=True, exist_ok=True)
    
    class_names = validate_dataset(str(dataset_dir))
    
    # Generate class_names.json
    with open(export_dir / "class_names.json", "w") as f:
        json.dump(class_names, f)
        
    print("Loading datasets with 70/15/15 split...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir, validation_split=0.3, subset="training", seed=42, 
        image_size=(224,224), batch_size=8, label_mode='categorical'
    )
    temp_val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir, validation_split=0.3, subset="validation", seed=42, 
        image_size=(224,224), batch_size=8, label_mode='categorical'
    )
    
    val_batches = tf.data.experimental.cardinality(temp_val_ds)
    test_ds = temp_val_ds.take(val_batches // 2)
    val_ds = temp_val_ds.skip(val_batches // 2)
    
    data_aug = get_data_augmentation()
    AUTOTUNE = tf.data.AUTOTUNE
    
    train_ds = train_ds.map(lambda x, y: (data_aug(x, training=True), y), num_parallel_calls=AUTOTUNE)
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.take(10).cache().prefetch(buffer_size=AUTOTUNE)
    
    # Compute class weights
    y = []
    for class_name in class_names:
        class_path = dataset_dir / class_name
        count = len([f for f in os.listdir(class_path) if f.lower().endswith(('.jpg','.jpeg','.png'))])
        y.extend([class_names.index(class_name)] * count)
        
    classes = np.unique(y)
    weights = compute_class_weight('balanced', classes=classes, y=y)
    class_weights = dict(zip(classes, weights))
    
    models_to_train = ["mobilenetv3", "efficientnetb0", "resnet50"]
    registry = {}
    best_score = -1
    best_model = None
    
    for m_name in models_to_train:
        print(f"\n--- Training {m_name} ---")
        model = build_model(len(class_names), m_name)
        
        filepath = export_dir / f"{m_name}_best.keras"
        callbacks = [
            tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True),
            tf.keras.callbacks.ModelCheckpoint(filepath=str(filepath), monitor='val_accuracy', save_best_only=True),
            tf.keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
        ]
        
        start_time = time.time()
        model.fit(train_ds, validation_data=val_ds, epochs=1, steps_per_epoch=20, validation_steps=5, callbacks=callbacks, class_weight=class_weights)
        train_time = time.time() - start_time
        
        if not filepath.exists():
            model.save(str(filepath))
            
        print(f"Evaluating {m_name} on test set...")
        y_true, y_pred, y_scores = [], [], []
        for x, y_batch in test_ds:
            preds = model.predict(x, verbose=0)
            y_true.extend(np.argmax(y_batch, axis=1))
            y_pred.extend(np.argmax(preds, axis=1))
            y_scores.extend(preds)
            
        y_true, y_pred, y_scores = np.array(y_true), np.array(y_pred), np.array(y_scores)
        
        acc = float(np.mean(y_true == y_pred))
        f1 = float(f1_score(y_true, y_pred, average='weighted', zero_division=0))
        prec = float(precision_score(y_true, y_pred, average='weighted', zero_division=0))
        rec = float(recall_score(y_true, y_pred, average='weighted', zero_division=0))
        
        top3_preds = np.argsort(y_scores, axis=1)[:, -3:]
        top3_acc = float(np.mean([y_true[i] in top3_preds[i] for i in range(len(y_true))]))
        
        cm = confusion_matrix(y_true, y_pred)
        per_class_acc = cm.diagonal() / np.maximum(cm.sum(axis=1), 1)
        poor = [class_names[i] for i, a in enumerate(per_class_acc) if a < 0.5]
        
        score = (acc + f1) / 2
        print(f"{m_name} Test Acc: {acc:.4f} | F1: {f1:.4f} | Score: {score:.4f}")
        
        registry[m_name] = {
            "test_accuracy": acc, "top3_accuracy": top3_acc,
            "precision": prec, "recall": rec, "f1_score": f1,
            "training_time": train_time, "poor_classes": poor
        }
        
        if score > best_score:
            best_score = score
            best_model = m_name
            
    print(f"\nBest Model: {best_model} with score {best_score:.4f}")
    best_src = export_dir / f"{best_model}_best.keras"
    best_dst = export_dir / "disease_production_best.keras"
    shutil.copy(best_src, best_dst)
    
    metadata = {
        "dataset_path": str(dataset_dir),
        "num_classes": len(class_names),
        "total_images": len(y),
        "split": "70/15/15",
        "best_architecture": best_model,
        "epochs": 1,
        "evaluation_metrics": registry,
        "best_model_metrics": registry[best_model],
        "training_timestamp": datetime.datetime.now().isoformat()
    }
    
    with open(export_dir / "training_metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
        
    print("Done! Model exported to", best_dst)

if __name__ == "__main__":
    main()
