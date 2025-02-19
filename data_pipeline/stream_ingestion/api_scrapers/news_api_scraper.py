import requests
import logging
import time
from requests.exceptions import HTTPError, ConnectionError, Timeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('news_api_scraper.log'), logging.StreamHandler()]
)

class NewsAPIScraper:
    def __init__(self, config):
        self.news_api_key = config['news_api_key']
        self.gnews_api_key = config['gnews_api_key']
        self.retry_limit = config.get('retry_limit', 3)
        logging.info("Initialized NewsAPIScraper.")

    def fetch_newsapi_articles(self, query, page_size=10):
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": query,
            "pageSize": page_size,
            "apiKey": self.news_api_key
        }
        return self._make_request(url, params, "NewsAPI")

    def fetch_gnews_articles(self, query, max_results=10):
        url = "https://gnews.io/api/v4/search"
        params = {
            "q": query,
            "max": max_results,
            "token": self.gnews_api_key
        }
        return self._make_request(url, params, "GNews")

    def _make_request(self, url, params, source_name):
        retries = 0
        while retries < self.retry_limit:
            try:
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                logging.info(f"Fetched {len(data.get('articles', []))} articles from {source_name}.")
                return data
            except (HTTPError, ConnectionError, Timeout) as e:
                logging.warning(f"{source_name} API error: {e}. Retrying ({retries + 1}/{self.retry_limit})...")
                retries += 1
                time.sleep(2 ** retries)
        logging.error(f"{source_name} API request failed after retries.")
        return None

if __name__ == "__main__":
    CONFIG = {
        "news_api_key": "YOUR_NEWSAPI_KEY",
        "gnews_api_key": "YOUR_GNEWS_API_KEY",
        "retry_limit": 5
    }

    scraper = NewsAPIScraper(CONFIG)
    newsapi_articles = scraper.fetch_newsapi_articles(query="misinformation", page_size=20)
    gnews_articles = scraper.fetch_gnews_articles(query="fake news", max_results=15)
