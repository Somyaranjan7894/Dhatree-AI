import os
from pathlib import Path
import tensorflow as tf
from tensorflow.keras import layers

import numpy as np

def get_data_augmentation(image_size: tuple = (224, 224)):
    """
    Returns a Sequential model with standard data augmentation layers.
    Includes flip, rotation, zoom, contrast, brightness, and translation.
    """
    return tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomContrast(0.2),
        layers.RandomBrightness(0.2),
        layers.RandomTranslation(height_factor=0.1, width_factor=0.1)
    ], name="data_augmentation")

def compute_class_weights(data_dir: str):
    """
    Computes class weights to handle dataset imbalance.
    """
    import os
    from sklearn.utils.class_weight import compute_class_weight

    class_names = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))])
    y = []
    for i, class_name in enumerate(class_names):
        class_path = os.path.join(data_dir, class_name)
        count = len([f for f in os.listdir(class_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.JPG', '.JPEG'))])
        y.extend([i] * count)
    
    if not y:
        return None

    classes = np.unique(y)
    weights = compute_class_weight('balanced', classes=classes, y=y)
    return dict(zip(classes, weights))

def load_plantvillage_dataset(data_dir: str, image_size: tuple = (224, 224), batch_size: int = 32, validation_split: float = 0.2, seed: int = 42, augment: bool = True):
    """
    Loads and splits the PlantVillage dataset into training, validation, and test sets.
    """
    data_path = Path(data_dir)
    
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset directory not found: {data_path}")

    print(f"Loading dataset from: {data_path}")

    train_ds = tf.keras.utils.image_dataset_from_directory(
        data_path,
        validation_split=validation_split,
        subset="training",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode='categorical'
    )

    temp_val_ds = tf.keras.utils.image_dataset_from_directory(
        data_path,
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode='categorical'
    )

    class_names = train_ds.class_names
    print(f"Found {len(class_names)} classes: {class_names}")

    # Split the validation subset into 50% validation and 50% test
    val_batches = tf.data.experimental.cardinality(temp_val_ds)
    test_ds = temp_val_ds.take(val_batches // 2)
    val_ds = temp_val_ds.skip(val_batches // 2)

    # Optimize datasets for performance
    AUTOTUNE = tf.data.AUTOTUNE
    
    if augment:
        data_augmentation = get_data_augmentation(image_size)
        train_ds = train_ds.map(lambda x, y: (data_augmentation(x, training=True), y), num_parallel_calls=AUTOTUNE)

    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, val_ds, test_ds, class_names
