from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np
from typing import List, Dict, Any, Union
from ai.utils.logger import ai_logger

class ModelEvaluator:
    """
    Reusable evaluation utilities using scikit-learn.
    Outputs standardized performance metrics.
    """
    
    @staticmethod
    def evaluate_classification(y_true: Union[List[int], np.ndarray], 
                                y_pred: Union[List[int], np.ndarray], 
                                target_names: List[str] = None) -> Dict[str, Any]:
        """
        Computes comprehensive classification metrics.
        """
        accuracy = accuracy_score(y_true, y_pred)
        precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
        
        conf_matrix = confusion_matrix(y_true, y_pred)
        
        report_str = classification_report(y_true, y_pred, target_names=target_names, zero_division=0)
        
        metrics = {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "confusion_matrix": conf_matrix.tolist()
        }
        
        ai_logger.info("Classification Evaluation Complete")
        ai_logger.info(f"Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
        
        return {
            "metrics": metrics,
            "report_string": report_str
        }
