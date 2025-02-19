from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
import numpy as np
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class OnlineTrainer:
    """
    Online learning module for real-time model updates using SGDClassifier.
    """

    def __init__(self, model: SGDClassifier = None):
        """
        Initializes the online trainer.

        Args:
            model (SGDClassifier): An instance of SGDClassifier for incremental learning.
        """
        self.model = model or SGDClassifier(loss='log_loss', learning_rate='optimal')
        self.scaler = StandardScaler()
        self.is_fitted = False

    def partial_fit(self, X_batch: np.ndarray, y_batch: np.ndarray, classes: np.ndarray = None) -> None:
        """
        Updates the model incrementally with a batch of new data.

        Args:
            X_batch (np.ndarray): Feature batch.
            y_batch (np.ndarray): Label batch.
            classes (np.ndarray): All possible class labels (required for first fit).
        """
        X_scaled = self.scaler.fit_transform(X_batch) if not self.is_fitted else self.scaler.transform(X_batch)
        self.is_fitted = True

        if not hasattr(self.model, "classes_"):
            self.model.partial_fit(X_scaled, y_batch, classes=classes)
        else:
            self.model.partial_fit(X_scaled, y_batch)

        logging.info(f"Model incrementally updated with batch of size {X_batch.shape[0]}.")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Makes predictions on new data.

        Args:
            X (np.ndarray): Feature data.

        Returns:
            np.ndarray: Predicted labels.
        """
        if not self.is_fitted:
            raise ValueError("Model has not been trained yet.")
        X_scaled = self.scaler.transform(X)
        return self.model.predict(X_scaled)


if __name__ == "__main__":
    from sklearn.datasets import make_classification

    X_stream, y_stream = make_classification(n_samples=1000, n_features=20, random_state=42)
    trainer = OnlineTrainer()

    batch_size = 50
    for i in range(0, len(X_stream), batch_size):
        X_batch = X_stream[i:i+batch_size]
        y_batch = y_stream[i:i+batch_size]
        trainer.partial_fit(X_batch, y_batch, classes=np.array([0, 1]))

    # Testing predictions
    X_test, _ = make_classification(n_samples=5, n_features=20, random_state=42)
    predictions = trainer.predict(X_test)
    logging.info(f"Predictions on new data: {predictions}")
