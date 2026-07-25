import os
import json
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, log_loss
from sklearn.metrics import cohen_kappa_score, matthews_corrcoef, confusion_matrix, classification_report
from pathlib import Path

# Fix memory growth for mixed precision/GPU
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        policy = tf.keras.mixed_precision.Policy('mixed_float16')
        tf.keras.mixed_precision.set_global_policy(policy)
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
    except Exception as e:
        print(f"GPU config error: {e}")

def load_test_dataset(data_dir, image_size=(224, 224), batch_size=32, validation_split=0.3, seed=42):
    print(f"Loading dataset from: {data_dir}")
    temp_val_ds = tf.keras.utils.image_dataset_from_directory(
        data_dir,
        validation_split=validation_split,
        subset="validation",
        seed=seed,
        image_size=image_size,
        batch_size=batch_size,
        label_mode='categorical',
        shuffle=True
    )
    class_names = temp_val_ds.class_names
    # Split val into 50% val, 50% test. We want the test part (last 50%)
    val_batches = tf.data.experimental.cardinality(temp_val_ds)
    test_ds = temp_val_ds.take(val_batches // 2)
    # Cache and prefetch
    AUTOTUNE = tf.data.AUTOTUNE
    test_ds = test_ds.cache().prefetch(buffer_size=AUTOTUNE)
    return test_ds, class_names

def main():
    base_dir = Path("c:/Users/SOUMYA RANJAN BEHERA/OneDrive/Desktop/dhatree_AI")
    model_dir = base_dir / "ai" / "models" / "disease_detection"
    reports_dir = base_dir / "reports"
    eval_reports_dir = reports_dir / "evaluation"
    eval_reports_dir.mkdir(parents=True, exist_ok=True)
    
    with open(model_dir / "training_metadata.json", "r") as f:
        metadata = json.load(f)
        
    data_dir = metadata.get("dataset_path", str(base_dir / "ai" / "datasets" / "raw" / "plantvillage"))
    
    with open(model_dir / "class_names.json", "r") as f:
        class_names = json.load(f)
        
    print("Loading test dataset...")
    test_ds, ds_class_names = load_test_dataset(data_dir, validation_split=0.3)
    
    print("Loading model...")
    model = tf.keras.models.load_model(model_dir / "disease_production_best.keras", compile=False)
    
    # Get true labels and predictions
    y_true_all = []
    y_pred_all = []
    y_prob_all = []
    
    print("Running inference on test dataset...")
    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true_all.extend(np.argmax(labels.numpy(), axis=1))
        y_prob_all.extend(preds)
        y_pred_all.extend(np.argmax(preds, axis=1))
        
    y_true_all = np.array(y_true_all)
    y_pred_all = np.array(y_pred_all)
    y_prob_all = np.array(y_prob_all)
    
    print("Calculating overall metrics...")
    test_acc = accuracy_score(y_true_all, y_pred_all)
    
    # Top-3 Accuracy
    top3_correct = 0
    for true, prob in zip(y_true_all, y_prob_all):
        top3_preds = np.argsort(prob)[-3:]
        if true in top3_preds:
            top3_correct += 1
    top3_acc = top3_correct / len(y_true_all)
    
    # Precision, Recall, F1 (Macro)
    p_mac, r_mac, f1_mac, _ = precision_recall_fscore_support(y_true_all, y_pred_all, average='macro')
    # Precision, Recall, F1 (Weighted)
    p_wt, r_wt, f1_wt, _ = precision_recall_fscore_support(y_true_all, y_pred_all, average='weighted')
    
    loss = log_loss(y_true_all, y_prob_all, labels=range(len(class_names)))
    kappa = cohen_kappa_score(y_true_all, y_pred_all)
    mcc = matthews_corrcoef(y_true_all, y_pred_all)
    
    overall_metrics = {
        "Test Accuracy": test_acc,
        "Top-1 Accuracy": test_acc,
        "Top-3 Accuracy": top3_acc,
        "Precision (Macro)": p_mac,
        "Precision (Weighted)": p_wt,
        "Recall (Macro)": r_mac,
        "Recall (Weighted)": r_wt,
        "F1 Score (Macro)": f1_mac,
        "F1 Score (Weighted)": f1_wt,
        "Loss": loss,
        "Cohen's Kappa": kappa,
        "MCC": mcc
    }
    
    with open(eval_reports_dir / "overall_metrics.json", "w") as f:
        json.dump(overall_metrics, f, indent=4)
        
    print("Calculating per-class performance...")
    p_cls, r_cls, f1_cls, support = precision_recall_fscore_support(y_true_all, y_pred_all, labels=range(len(class_names)))
    
    per_class_data = []
    for i, cls_name in enumerate(class_names):
        idx = np.where(y_true_all == i)[0]
        total_imgs = len(idx)
        if total_imgs > 0:
            correct = np.sum(y_pred_all[idx] == i)
            acc = float(correct) / total_imgs
        else:
            correct = 0
            acc = 0.0
            
        per_class_data.append({
            "Class": cls_name,
            "Total Images": total_imgs,
            "Correct Predictions": correct,
            "Accuracy": acc,
            "Precision": p_cls[i],
            "Recall": r_cls[i],
            "F1 Score": f1_cls[i]
        })
        
    df_per_class = pd.DataFrame(per_class_data)
    df_per_class = df_per_class.sort_values(by="Accuracy")
    
    # Recommendations for Accuracy < 95%
    df_per_class["Needs Improvement"] = df_per_class["Accuracy"] < 0.95
    df_per_class["Recommendation"] = df_per_class["Needs Improvement"].apply(
        lambda x: "Add more varied samples, utilize harder augmentations, or check mislabeled data." if x else "Good"
    )
    
    df_per_class.to_csv(eval_reports_dir / "per_class_metrics.csv", index=False)
    
    with open(eval_reports_dir / "per_class_metrics.md", "w") as f:
        f.write("# Per-Class Performance\n\n")
        f.write(df_per_class.to_markdown(index=False))
        
    print("Generating Confusion Matrix...")
    cm = confusion_matrix(y_true_all, y_pred_all)
    plt.figure(figsize=(24, 20))
    sns.heatmap(cm, annot=False, cmap='Blues', xticklabels=class_names, yticklabels=class_names)
    plt.title("Confusion Matrix")
    plt.ylabel('True Class')
    plt.xlabel('Predicted Class')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    plt.savefig(eval_reports_dir / "confusion_matrix.png", dpi=300)
    plt.savefig(eval_reports_dir / "confusion_matrix.pdf")
    plt.close()
    
    print("Generating Classification Report...")
    clf_report = classification_report(y_true_all, y_pred_all, target_names=class_names, output_dict=True)
    df_clf = pd.DataFrame(clf_report).transpose()
    df_clf.to_csv(eval_reports_dir / "classification_report.csv")
    
    with open(eval_reports_dir / "classification_report.md", "w") as f:
        f.write("# Classification Report\n\n")
        f.write(df_clf.to_markdown())
        
    print("Evaluation phase completed successfully!")

if __name__ == "__main__":
    main()
