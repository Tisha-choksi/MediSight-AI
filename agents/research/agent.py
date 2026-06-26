import pandas as pd
from agents.clinical_evidence.agent import ClinicalEvidenceAgent


class ResearchAgent:
    def __init__(self):
        self.models = ["resnet50", "efficientnet", "convnext", "vit"]
        self.experiments = []

    def run_experiments(self, train_data, test_data) -> pd.DataFrame:
        results = []
        for model_name in self.models:
            agent = ClinicalEvidenceAgent()
            y_true, y_pred, y_proba = self._train_and_evaluate(model_name, train_data, test_data)
            metrics = agent.evaluate(y_true, y_pred, y_proba)
            metrics["model_name"] = model_name
            results.append(metrics)
            self.experiments.append(metrics)

        leaderboard = pd.DataFrame(results).sort_values("accuracy", ascending=False)
        self._generate_report(leaderboard)
        return leaderboard

    def _train_and_evaluate(self, model_name: str, train_data, test_data):
        # Placeholder: actual training happens here
        import numpy as np
        y_true = np.random.randint(0, 2, 100)
        y_pred = np.random.randint(0, 2, 100)
        y_proba = np.random.rand(100)
        return y_true, y_pred, y_proba

    def _generate_report(self, leaderboard: pd.DataFrame):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(leaderboard["model_name"], leaderboard["accuracy"])
        ax.set_title("Model Comparison - Accuracy")
        ax.set_ylabel("Accuracy (%)")
        fig.savefig("best_model_report.pdf")
        plt.close(fig)
