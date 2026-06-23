import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, roc_auc_score, confusion_matrix,
)


class ClinicalEvidenceAgent:
    def __init__(self):
        self.metrics = {}

    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray, y_proba: np.ndarray) -> dict:
        self.metrics = {
            "accuracy": round(accuracy_score(y_true, y_pred) * 100, 2),
            "precision": round(precision_score(y_true, y_pred, average="binary") * 100, 2),
            "recall": round(recall_score(y_true, y_pred, average="binary") * 100, 2),
            "f1": round(f1_score(y_true, y_pred, average="binary") * 100, 2),
            "roc_auc": round(roc_auc_score(y_true, y_proba), 2),
        }
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()
        self.metrics["sensitivity"] = round(tp / (tp + fn) * 100, 2)
        self.metrics["specificity"] = round(tn / (tn + fp) * 100, 2)
        return self.metrics
