import re
import logging
from urllib.parse import urlparse, urlunparse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('url_extractor.log'), logging.StreamHandler()]
)

class URLExtractor:
    URL_PATTERN = re.compile(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+[^\s]*')

    def __init__(self):
        logging.info("Initialized URLExtractor.")

    def extract_urls(self, text):
        logging.info("Extracting URLs from text.")
        raw_urls = self.URL_PATTERN.findall(text)
        normalized_urls = {self._normalize_url(url) for url in raw_urls}
        logging.info(f"Extracted {len(normalized_urls)} unique URLs.")
        return list(normalized_urls)

    @staticmethod
    def _normalize_url(url):
        parsed_url = urlparse(url)
        normalized = parsed_url._replace(query="", fragment="")
        return urlunparse(normalized)

if __name__ == "__main__":
    extractor = URLExtractor()
    sample_text = "Check out https://example.com and http://test-site.com/path?query=value#fragment."
    urls = extractor.extract_urls(sample_text)
    print(urls)

