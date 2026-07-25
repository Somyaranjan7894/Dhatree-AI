import os
import json
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tensorflow as tf
from pathlib import Path

# Fix memory growth
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        policy = tf.keras.mixed_precision.Policy('mixed_float16')
        tf.keras.mixed_precision.set_global_policy(policy)
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except Exception as e:
        print(f"GPU config error: {e}")

def get_img_array(img_path, size):
    img = tf.keras.utils.load_img(img_path, target_size=size)
    array = tf.keras.utils.img_to_array(img)
    array = np.expand_dims(array, axis=0)
    return array

def make_gradcam_heatmap(img_array, model, last_conv_layer_name, pred_index=None):
    grad_model = tf.keras.models.Model(
        inputs=model.inputs, outputs=[model.get_layer(last_conv_layer_name).output, model.output]
    )

    with tf.GradientTape() as tape:
        last_conv_layer_output, preds = grad_model(img_array)
        if pred_index is None:
            pred_index = tf.argmax(preds[0])
        class_channel = preds[:, pred_index]

    grads = tape.gradient(class_channel, last_conv_layer_output)
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    last_conv_layer_output = last_conv_layer_output[0]
    heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
    heatmap = tf.squeeze(heatmap)

    heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
    return heatmap.numpy()

def save_and_display_gradcam(img_path, heatmap, cam_path="cam.jpg", alpha=0.4):
    img = cv2.imread(img_path)
    heatmap = cv2.resize(heatmap, (img.shape[1], img.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
    superimposed_img = heatmap * alpha + img
    superimposed_img = np.clip(superimposed_img, 0, 255).astype(np.uint8)
    cv2.imwrite(cam_path, superimposed_img)

def main():
    base_dir = Path("c:/Users/SOUMYA RANJAN BEHERA/OneDrive/Desktop/dhatree_AI")
    model_dir = base_dir / "ai" / "models" / "disease_detection"
    reports_dir = base_dir / "reports" / "gradcam"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    model_path = model_dir / "disease_production_best.keras"
    print("Loading model for Grad-CAM...")
    model = tf.keras.models.load_model(model_path, compile=False)
    
    # Find last conv layer
    # Since model is constructed as base_model -> GlobalAveragePooling -> Dropout -> Dense,
    # the base_model is a Functional layer
    base_model = None
    for layer in model.layers:
        if isinstance(layer, tf.keras.Model):
            base_model = layer
            break
            
    if base_model is None:
        print("Could not find base model. Trying to find last conv layer directly.")
        last_conv_layer = None
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer.name
                break
    else:
        last_conv_layer = None
        for layer in reversed(base_model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer.name
                break
        # Flatten base model into main model or wrap for gradcam
        # Actually, it's easier to use the inner model if base_model exists.
        # But we need preprocessing too if it's outside. In this codebase, preprocessing is done before base_model inside `model`.
        pass
        
    # Build a flattened version of the model to easily access the conv layer
    # Wait, if base_model is inside model, `model.get_layer(last_conv_layer)` will fail.
    # We must do gradcam on `model`. 
    # Let's just find the `base_model` name.
    
    # For now, let's just do an end-to-end trace.
    print(f"Model layers: {[l.name for l in model.layers]}")
    # We will write the robust gradcam logic that handles nested models.
    def get_nested_conv_layer(m):
        for layer in reversed(m.layers):
            if isinstance(layer, tf.keras.Model):
                return get_nested_conv_layer(layer)
            if isinstance(layer, tf.keras.layers.Conv2D):
                return layer.name, m
        return None, m

    conv_layer_name, inner_model = get_nested_conv_layer(model)
    print(f"Using conv layer {conv_layer_name} from model {inner_model.name}")
    
    with open(model_dir / "training_metadata.json", "r") as f:
        metadata = json.load(f)
    data_dir = Path(metadata.get("dataset_path", str(base_dir / "ai" / "datasets" / "raw" / "plantvillage")))
    with open(model_dir / "class_names.json", "r") as f:
        class_names = json.load(f)

    # Let's sample images
    # We just need a few images. Let's take the first batch from test set.
    temp_val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=0.3,
        subset="validation",
        seed=42,
        image_size=(224, 224),
        batch_size=32,
        label_mode='categorical',
        shuffle=False
    )
    val_batches = tf.data.experimental.cardinality(temp_val_ds)
    test_ds = temp_val_ds.take(val_batches // 2)
    
    # Gather some images and paths
    # `image_dataset_from_directory` stores file paths in `.file_paths`
    file_paths = temp_val_ds.file_paths
    test_paths = file_paths[:len(file_paths)//2]
    
    # We will pick 1 image per class and generate grad-cam
    sampled_classes = set()
    images_processed = 0
    
    for i, path in enumerate(test_paths):
        true_class = path.split(os.sep)[-2]
        if true_class in sampled_classes:
            continue
            
        img_array = get_img_array(path, size=(224, 224))
        preds = model.predict(img_array, verbose=0)
        pred_idx = np.argmax(preds[0])
        pred_class = class_names[pred_idx]
        
        # We need a unified model to get gradients if nested
        # Actually it's easier to use tf.GradientTape directly on the top-level model by watching the intermediate output.
        # But top level model doesn't expose inner layer output directly.
        # A simple hack is to modify the model to output the intermediate.
        # Let's skip pure Grad-CAM if too complex for nested, or use standard method if we can extract it.
        # For ResNet50 inside a Sequential/Functional, we can construct a new model:
        
        try:
            if inner_model != model:
                # model = Input -> Preprocess -> InnerModel -> Pooling -> Dense
                # We can trace it by getting the intermediate inner_model output
                grad_model = tf.keras.models.Model(
                    inputs=inner_model.inputs, outputs=[inner_model.get_layer(conv_layer_name).output, inner_model.output]
                )
                with tf.GradientTape() as tape:
                    # Need to preprocess manually because preprocessing is OUTSIDE inner_model
                    # Let's just pass img_array through the layers before inner_model
                    x = img_array
                    for layer in model.layers:
                        if layer == inner_model:
                            break
                        if isinstance(layer, tf.keras.layers.InputLayer):
                            continue
                        x = layer(x)
                        
                    last_conv_layer_output, inner_preds = grad_model(x)
                    # Now pass inner_preds through remaining layers
                    x2 = inner_preds
                    started = False
                    for layer in model.layers:
                        if started:
                            x2 = layer(x2)
                        if layer == inner_model:
                            started = True
                    preds2 = x2
                    class_channel = preds2[:, pred_idx]

                grads = tape.gradient(class_channel, last_conv_layer_output)
                pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
                last_conv_layer_output = last_conv_layer_output[0]
                heatmap = last_conv_layer_output @ pooled_grads[..., tf.newaxis]
                heatmap = tf.squeeze(heatmap)
                heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
                heatmap = heatmap.numpy()
            else:
                heatmap = make_gradcam_heatmap(img_array, model, conv_layer_name, pred_idx)
                
            out_name = f"{true_class}_pred_{pred_class}.jpg"
            save_and_display_gradcam(path, heatmap, str(reports_dir / out_name))
            sampled_classes.add(true_class)
            images_processed += 1
            if images_processed >= len(class_names):
                break
        except Exception as e:
            import traceback
            print(f"Error generating Grad-CAM for {path}: {e}")
            traceback.print_exc()
            
    print("Grad-CAM generation complete.")

if __name__ == "__main__":
    main()
