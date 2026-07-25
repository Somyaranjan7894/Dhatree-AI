import argparse
import time
import os
import psutil
import json
import numpy as np
import tensorflow as tf
from pathlib import Path

def benchmark_performance(model_path: str, output_dir: str):
    print(f"--- Benchmarking Performance ---")
    
    output_path = Path(output_dir)
    m_path = Path(model_path)
    
    if not m_path.exists():
        raise FileNotFoundError(f"Model not found at {m_path}")
        
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss / (1024 * 1024)
    
    print("Measuring load time...")
    t0 = time.time()
    model = tf.keras.models.load_model(str(m_path))
    t1 = time.time()
    load_time = t1 - t0
    
    mem_after = process.memory_info().rss / (1024 * 1024)
    ram_usage = mem_after - mem_before
    
    file_size_mb = os.path.getsize(str(m_path)) / (1024 * 1024)
    
    print("Measuring inference latency (100 iterations)...")
    dummy_input = np.random.rand(1, 224, 224, 3).astype(np.float32)
    
    # Warmup
    for _ in range(5):
        model.predict(dummy_input, verbose=0)
        
    latencies = []
    for _ in range(100):
        t0 = time.time()
        model.predict(dummy_input, verbose=0)
        t1 = time.time()
        latencies.append((t1 - t0) * 1000) # milliseconds
        
    avg_latency = np.mean(latencies)
    p95_latency = np.percentile(latencies, 95)
    
    print("\n--- Benchmark Results ---")
    print(f"Model File Size: {file_size_mb:.2f} MB")
    print(f"Model Load Time: {load_time:.2f} seconds")
    print(f"Memory Increment: {ram_usage:.2f} MB")
    print(f"Average Inference Latency (Batch=1): {avg_latency:.2f} ms")
    print(f"95th Percentile Latency: {p95_latency:.2f} ms")
    
    benchmark_data = {
        "model_file_size_mb": file_size_mb,
        "load_time_seconds": load_time,
        "ram_usage_increment_mb": ram_usage,
        "avg_inference_latency_ms": avg_latency,
        "p95_inference_latency_ms": p95_latency
    }
    
    with open(output_path / "benchmark_results.json", "w") as f:
        json.dump(benchmark_data, f, indent=4)
        
    print(f"Benchmark results saved to {output_path / 'benchmark_results.json'}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark Production Model")
    parser.add_argument("--model_path", type=str, default="ai/models/artifacts/disease_production_best.keras")
    parser.add_argument("--output_dir", type=str, default="ai/models/artifacts")
    args = parser.parse_args()
    
    benchmark_performance(args.model_path, args.output_dir)
