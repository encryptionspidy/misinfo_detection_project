import logging
import numpy as np
from sklearn.ensemble import VotingClassifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EnsembleManager:
    """
    Manages ensemble learning techniques to combine predictions from multiple models for misinformation detection.
    """

    def __init__(self, models: dict):
        """
        Initializes the ensemble manager with a dictionary of models.

        Args:
            models (dict): A dictionary of models in the format {model_name: model_instance}.
        """
        self.models = models
        self.ensemble_model = None
        logging.info(f"Initialized EnsembleManager with models: {list(models.keys())}")

    def create_voting_classifier(self, voting_type='soft'):
        """
        Creates a voting classifier to combine model predictions.

        Args:
            voting_type (str): 'soft' for probability averaging, 'hard' for majority voting.
        """
        estimators = [(name, model) for name, model in self.models.items()]
        self.ensemble_model = VotingClassifier(estimators=estimators, voting=voting_type)
        logging.info(f"Voting classifier created with voting type: {voting_type}")

    def train_ensemble(self, X_train, y_train):
        """
        Trains the ensemble model on the provided data.

        Args:
            X_train (np.array): Training features.
            y_train (np.array): Training labels.
        """
        if self.ensemble_model is None:
            raise ValueError("Ensemble model has not been initialized. Run create_voting_classifier first.")
        logging.info("Training ensemble model...")
        self.ensemble_model.fit(X_train, y_train)
        logging.info("Ensemble model training complete.")

    def predict(self, X_test):
        """
        Predicts labels for test data using the trained ensemble model.

        Args:
            X_test (np.array): Test features.

        Returns:
            np.array: Predicted labels.
        """
        if self.ensemble_model is None:
            raise ValueError("Ensemble model is not trained yet.")
        logging.info("Making predictions with ensemble model...")
        return self.ensemble_model.predict(X_test)


if __name__ == "__main__":
    from sklearn.linear_model import LogisticRegression
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.svm import SVC

    # Example models
    models = {
        'log_reg': LogisticRegression(),
        'naive_bayes': MultinomialNB(),
        'svm': SVC(probability=True)
    }

    ensemble_manager = EnsembleManager(models)
    ensemble_manager.create_voting_classifier()

    # Dummy data for demonstration
    X_train, y_train = np.random.rand(100, 5), np.random.randint(0, 2, 100)
    ensemble_manager.train_ensemble(X_train, y_train)
    predictions = ensemble_manager.predict(np.random.rand(10, 5))
    print(predictions)
