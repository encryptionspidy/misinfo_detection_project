import logging
import joblib
from urllib.parse import urlparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MaliciousURLModel:
    """
    Loads a pre-trained model for detecting malicious URLs.
    """

    def __init__(self, model_path: str = "./models/url_model.joblib"):
        """
        Initializes the MaliciousURLModel with a specified model path.

        Args:
            model_path (str): Path to the saved model.
        """
        self.model_path = model_path
        self.model = None

    def load_model(self):
        """
        Loads the pre-trained model from disk.
        """
        try:
            logging.info(f"Loading malicious URL detection model from {self.model_path}...")
            self.model = joblib.load(self.model_path)
            logging.info("Model loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load model: {e}")
            raise
        return self

    def extract_features(self, url: str):
        """
        Extracts basic features from a URL for prediction.

        Args:
            url (str): The URL to analyze.

        Returns:
            list: Feature vector for the URL.
        """
        parsed_url = urlparse(url)
        features = [
            len(url),
            int(parsed_url.scheme == "https"),
            len(parsed_url.netloc),
            len(parsed_url.path),
            url.count('.'),
        ]
        return features

    def predict(self, url: str):
        """
        Predicts whether a URL is malicious.

        Args:
            url (str): The URL to classify.

        Returns:
            int: 1 if malicious, 0 otherwise.
        """
        if self.model is None:
            raise ValueError("Model is not loaded. Call load_model() first.")
        
        features = [self.extract_features(url)]
        prediction = self.model.predict(features)[0]
        return prediction


if __name__ == "__main__":
    url_model = MaliciousURLModel().load_model()
    result = url_model.predict("http://example.com")
    print(f"Is malicious: {result}")
