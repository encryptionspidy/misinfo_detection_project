import feedparser
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('broadcast_feed_scraper.log'), logging.StreamHandler()]
)

class BroadcastFeedScraper:
    def __init__(self, feed_urls, retry_limit=3):
        self.feed_urls = feed_urls
        self.retry_limit = retry_limit
        logging.info("Initialized BroadcastFeedScraper.")

    def fetch_feeds(self):
        all_feeds = []
        for url in self.feed_urls:
            retries = 0
            while retries < self.retry_limit:
                try:
                    feed = feedparser.parse(url)
                    if feed.entries:
                        logging.info(f"Fetched {len(feed.entries)} entries from {url}.")
                        all_feeds.extend(feed.entries)
                        break
                    else:
                        raise ValueError("No entries found.")
                except Exception as e:
                    logging.warning(f"Feed error for {url}: {e}. Retrying ({retries + 1}/{self.retry_limit})...")
                    retries += 1
                    time.sleep(2 ** retries)
        if not all_feeds:
            logging.error("No feeds were fetched from the provided URLs.")
        return all_feeds

if __name__ == "__main__":
    FEED_URLS = [
        "http://feeds.bbci.co.uk/news/rss.xml",
        "https://rss.cnn.com/rss/edition.rss"
    ]

    scraper = BroadcastFeedScraper(FEED_URLS)
    feeds = scraper.fetch_feeds()
