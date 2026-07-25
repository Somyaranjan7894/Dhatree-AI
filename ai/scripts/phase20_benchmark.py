import time
import json
import psutil
import numpy as np
import tensorflow as tf
from pathlib import Path
import tracemalloc

def benchmark_inference(model, images, device_name):
    latencies = []
    
    # Warmup
    print(f"[{device_name}] Warming up...")
    for i in range(5):
        _ = model.predict(tf.expand_dims(images[0], axis=0), verbose=0)
        
    print(f"[{device_name}] Running inference benchmark...")
    for img in images:
        start_time = time.time()
        _ = model.predict(tf.expand_dims(img, axis=0), verbose=0)
        latencies.append((time.time() - start_time) * 1000) # ms
        
    latencies = np.array(latencies)
    avg_latency = np.mean(latencies)
    median_latency = np.median(latencies)
    p95_latency = np.percentile(latencies, 95)
    img_per_sec = 1000.0 / avg_latency
    
    return {
        "Average Latency (ms)": avg_latency,
        "Median Latency (ms)": median_latency,
        "P95 Latency (ms)": p95_latency,
        "Images/sec": img_per_sec
    }

def main():
    base_dir = Path("c:/Users/SOUMYA RANJAN BEHERA/OneDrive/Desktop/dhatree_AI")
    model_dir = base_dir / "ai" / "models" / "disease_detection"
    reports_dir = base_dir / "reports" / "benchmark"
    reports_dir.mkdir(parents=True, exist_ok=True)
    
    print("Loading model...")
    model = tf.keras.models.load_model(model_dir / "disease_production_best.keras", compile=False)
    
    with open(model_dir / "training_metadata.json", "r") as f:
        metadata = json.load(f)
    data_dir = metadata.get("dataset_path", str(base_dir / "ai" / "datasets" / "raw" / "plantvillage"))
    
    print("Loading sample images...")
    ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        image_size=(224, 224),
        batch_size=32,
        shuffle=True,
        seed=42
    )
    
    # Get 100 images for latency benchmark
    images_100 = []
    for imgs, _ in ds.take(4):
        for img in imgs:
            images_100.append(img)
            if len(images_100) == 100:
                break
        if len(images_100) == 100:
            break
            
    # Measure memory tracking
    tracemalloc.start()
    
    # Run CPU Benchmark
    # We can force CPU by placing the operation in tf.device('/CPU:0')
    with tf.device('/CPU:0'):
        cpu_metrics = benchmark_inference(model, images_100, "CPU")
        
    # Run GPU Benchmark if available
    gpu_metrics = None
    gpus = tf.config.list_physical_devices('GPU')
    if gpus:
        with tf.device('/GPU:0'):
            gpu_metrics = benchmark_inference(model, images_100, "GPU")
            
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    peak_ram_mb = peak / 10**6
    # Track overall process memory
    process = psutil.Process()
    mem_info = process.memory_info()
    overall_ram_mb = mem_info.rss / 10**6
    
    print("--- Stress Test (10,000 Inferences) ---")
    # For stress test we will duplicate the 100 images 100 times to avoid IO bottleneck
    stress_images = images_100 * 100
    start_stress = time.time()
    batch_size = 32
    # Convert to batched dataset for faster inference
    stress_ds = tf.data.Dataset.from_tensor_slices(stress_images).batch(batch_size)
    for batch in stress_ds:
        _ = model.predict(batch, verbose=0)
    stress_time = time.time() - start_stress
    
    final_metrics = {
        "CPU": cpu_metrics,
        "GPU": gpu_metrics,
        "Memory": {
            "Peak RAM Allocation (MB)": peak_ram_mb,
            "Total Process RAM (MB)": overall_ram_mb
        },
        "Stress Test (10,000 images)": {
            "Total Time (s)": stress_time,
            "Images/sec": 10000 / stress_time
        }
    }
    
    with open(reports_dir / "benchmark_metrics.json", "w") as f:
        json.dump(final_metrics, f, indent=4)
        
    print("Benchmark complete!")
    print(json.dumps(final_metrics, indent=2))

if __name__ == "__main__":
    main()
