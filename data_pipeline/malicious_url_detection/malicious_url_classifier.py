import logging
import joblib
from phishing_heuristic import PhishingHeuristic
from blacklist_checker import BlacklistChecker
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('malicious_url_classifier.log'), logging.StreamHandler()]
)

class MaliciousURLClassifier:
    def __init__(self, model_path='malicious_url_model.pkl', blacklist_path='blacklist.txt'):
        self.model = self._load_model(model_path)
        self.heuristic_checker = PhishingHeuristic()
        self.blacklist_checker = BlacklistChecker(local_blacklist_path=blacklist_path)
        logging.info("Initialized MaliciousURLClassifier.")

    def _load_model(self, model_path):
        logging.info(f"Loading ML model from {model_path}.")
        return joblib.load(model_path)

    def classify(self, url):
        logging.info(f"Classifying URL: {url}")

        # Blacklist Check
        if self.blacklist_checker.is_blacklisted(url):
            return 'Malicious', {'method': 'Blacklist'}

        # Heuristic Check
        phishing_detected, heuristics = self.heuristic_checker.is_phishing_url(url)
        if phishing_detected:
            return 'Malicious', {'method': 'Heuristic', 'details': heuristics}

        # ML Model Prediction
        features = self._extract_features(url)
        prediction = self.model.predict([features])[0]
        result = 'Malicious' if prediction == 1 else 'Safe'
        logging.info(f"ML model classified URL as: {result}")
        return result, {'method': 'ML', 'features': features}

    def _extract_features(self, url):
        parsed = urlparse(url)
        domain = parsed.netloc
        features = {
            'url_length': len(url),
            'num_dots': domain.count('.'),
            'num_slashes': url.count('/'),
            'has_ip_address': bool(re.match(r'\d+\.\d+\.\d+\.\d+', domain)),
        }
        return list(features.values())

if __name__ == "__main__":
    classifier = MaliciousURLClassifier()
    test_url = "http://example.com/login"
    result, details = classifier.classify(test_url)
    print(f"URL: {test_url} - Classification: {result}, Details: {details}")
