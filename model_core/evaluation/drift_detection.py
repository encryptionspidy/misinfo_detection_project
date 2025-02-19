import logging
import numpy as np
from scipy.stats import wasserstein_distance

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class DriftDetector:
    """
    Detects concept drift by comparing prediction distributions over time.
    """

    def __init__(self, threshold=0.1):
        """
        Initializes the drift detection module.

        Args:
            threshold (float): The Wasserstein distance threshold for detecting drift.
        """
        self.threshold = threshold
        self.reference_distribution = None

    def update_reference_distribution(self, predictions: np.ndarray):
        """
        Updates the reference prediction distribution.

        Args:
            predictions (np.ndarray): Historical model predictions.
        """
        self.reference_distribution = np.histogram(predictions, bins=10, density=True)[0]

    def detect_drift(self, new_predictions: np.ndarray):
        """
        Detects drift by comparing a new prediction distribution to the reference.

        Args:
            new_predictions (np.ndarray): Recent model predictions.

        Returns:
            bool: True if drift is detected, False otherwise.
        """
        if self.reference_distribution is None:
            logging.warning("Reference distribution not set. Updating it now.")
            self.update_reference_distribution(new_predictions)
            return False

        new_distribution = np.histogram(new_predictions, bins=10, density=True)[0]
        distance = wasserstein_distance(self.reference_distribution, new_distribution)

        logging.info(f"Wasserstein distance: {distance}")
        return distance > self.threshold


if __name__ == "__main__":
    detector = DriftDetector()
    
    # Simulating prediction distributions
    historical_preds = np.random.normal(0.5, 0.1, 1000)
    new_preds = np.random.normal(0.6, 0.1, 1000)

    detector.update_reference_distribution(historical_preds)
    drift_detected = detector.detect_drift(new_preds)
    print(f"Drift detected: {drift_detected}")
