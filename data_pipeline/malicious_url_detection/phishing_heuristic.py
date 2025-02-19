import re
import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('phishing_heuristic.log'), logging.StreamHandler()]
)

class PhishingHeuristic:
    SUSPICIOUS_KEYWORDS = ['login', 'verify', 'account', 'secure', 'update', 'confirm']
    IP_ADDRESS_PATTERN = re.compile(r'\b\d{1,3}(\.\d{1,3}){3}\b')

    def __init__(self):
        logging.info("Initialized PhishingHeuristic.")

    def is_phishing_url(self, url):
        logging.info(f"Applying heuristic checks for URL: {url}")
        parsed = urlparse(url)
        domain = parsed.netloc
        path = parsed.path

        heuristics = {
            'has_ip_address': bool(self.IP_ADDRESS_PATTERN.match(domain)),
            'contains_suspicious_keywords': any(keyword in url.lower() for keyword in self.SUSPICIOUS_KEYWORDS),
            'long_url': len(url) > 75,
            'subdomain_count': domain.count('.') > 3
        }

        is_phishing = any(heuristics.values())
        logging.info(f"Phishing detection heuristics for '{url}': {heuristics}. Result: {'Phishing' if is_phishing else 'Safe'}")
        return is_phishing, heuristics

if __name__ == "__main__":
    heuristic = PhishingHeuristic()
    test_url = "http://192.168.1.1/secure/login/update"
    print(heuristic.is_phishing_url(test_url))
