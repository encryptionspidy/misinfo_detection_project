import requests
import logging
import time
from requests.exceptions import HTTPError, ConnectionError, Timeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('social_feed_scraper.log'), logging.StreamHandler()]
)

class SocialFeedScraper:
    def __init__(self, config):
        self.twitter_bearer_token = config['twitter_bearer_token']
        self.reddit_client_id = config['reddit_client_id']
        self.reddit_secret = config['reddit_secret']
        self.headers = {"Authorization": f"Bearer {self.twitter_bearer_token}"}
        self.reddit_base_url = "https://www.reddit.com"
        self.twitter_base_url = "https://api.twitter.com/2/tweets/search/recent"
        self.retry_limit = config.get('retry_limit', 3)
        logging.info("Initialized SocialFeedScraper.")

    def fetch_twitter_data(self, query, max_results=10):
        params = {"query": query, "max_results": max_results}
        retries = 0
        while retries < self.retry_limit:
            try:
                response = requests.get(self.twitter_base_url, headers=self.headers, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                logging.info(f"Fetched {len(data.get('data', []))} tweets for query: {query}")
                return data
            except (HTTPError, ConnectionError, Timeout) as e:
                logging.warning(f"Twitter API error: {e}. Retrying ({retries + 1}/{self.retry_limit})...")
                retries += 1
                time.sleep(2 ** retries)
        logging.error("Twitter API request failed after retries.")
        return None

    def fetch_reddit_data(self, subreddit, limit=10):
        url = f"{self.reddit_base_url}/r/{subreddit}/new.json"
        auth = requests.auth.HTTPBasicAuth(self.reddit_client_id, self.reddit_secret)
        headers = {'User-Agent': 'misinfo-scraper/0.1'}
        retries = 0
        while retries < self.retry_limit:
            try:
                response = requests.get(url, auth=auth, headers=headers, params={"limit": limit}, timeout=10)
                response.raise_for_status()
                data = response.json()
                logging.info(f"Fetched {len(data.get('data', {}).get('children', []))} Reddit posts from r/{subreddit}")
                return data
            except (HTTPError, ConnectionError, Timeout) as e:
                logging.warning(f"Reddit API error: {e}. Retrying ({retries + 1}/{self.retry_limit})...")
                retries += 1
                time.sleep(2 ** retries)
        logging.error("Reddit API request failed after retries.")
        return None

if __name__ == "__main__":
    CONFIG = {
        "twitter_bearer_token": "YOUR_TWITTER_BEARER_TOKEN",
        "reddit_client_id": "YOUR_REDDIT_CLIENT_ID",
        "reddit_secret": "YOUR_REDDIT_SECRET",
        "retry_limit": 5
    }

    scraper = SocialFeedScraper(CONFIG)
    twitter_data = scraper.fetch_twitter_data(query="misinformation", max_results=20)
    reddit_data = scraper.fetch_reddit_data(subreddit="conspiracy", limit=15)
