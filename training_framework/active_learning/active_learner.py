import numpy as np
from sklearn.base import BaseEstimator
from typing import List, Tuple
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ActiveLearner:
    """
    Active Learning framework using uncertainty sampling.
    Selects the most uncertain samples to be labeled by humans.
    """

    def __init__(self, model: BaseEstimator, unlabeled_data: np.ndarray):
        """
        Initializes the active learner.

        Args:
            model (BaseEstimator): Pre-trained model for uncertainty estimation.
            unlabeled_data (np.ndarray): Unlabeled dataset for active learning.
        """
        self.model = model
        self.unlabeled_data = unlabeled_data

    def uncertainty_sampling(self, batch_size: int = 10) -> np.ndarray:
        """
        Selects the top N most uncertain samples based on prediction probabilities.

        Args:
            batch_size (int): Number of samples to query for labeling.

        Returns:
            np.ndarray: Indices of the selected samples.
        """
        # Get prediction probabilities for the unlabeled data
        proba = self.model.predict_proba(self.unlabeled_data)

        # Calculate uncertainty using entropy
        entropy = -np.sum(proba * np.log(proba + 1e-6), axis=1)
        uncertain_indices = np.argsort(entropy)[-batch_size:]

        logging.info(f"Selected {batch_size} most uncertain samples for labeling.")
        return uncertain_indices

    def update_model(self, labeled_data: np.ndarray, labels: np.ndarray) -> None:
        """
        Updates the model with newly labeled data.

        Args:
            labeled_data (np.ndarray): Newly labeled samples.
            labels (np.ndarray): Corresponding labels.
        """
        self.model.fit(labeled_data, labels)
        logging.info("Model updated with newly labeled data.")

    def run_active_learning(self, iterations: int = 5, batch_size: int = 10) -> None:
        """
        Runs the active learning process iteratively.

        Args:
            iterations (int): Number of active learning cycles.
            batch_size (int): Number of samples per iteration to query.
        """
        for i in range(iterations):
            logging.info(f"Active Learning Iteration: {i + 1}/{iterations}")
            uncertain_indices = self.uncertainty_sampling(batch_size)
            # Simulate human labeling (replace with actual human input in production)
            simulated_labels = np.random.randint(0, 2, size=batch_size)
            self.update_model(self.unlabeled_data[uncertain_indices], simulated_labels)

            # Remove labeled samples from unlabeled data
            self.unlabeled_data = np.delete(self.unlabeled_data, uncertain_indices, axis=0)


if __name__ == "__main__":
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.datasets import make_classification

    # Example setup
    X_unlabeled, _ = make_classification(n_samples=1000, n_features=20, random_state=42)
    model = RandomForestClassifier()

    learner = ActiveLearner(model=model, unlabeled_data=X_unlabeled)
    learner.run_active_learning(iterations=5, batch_size=20)
