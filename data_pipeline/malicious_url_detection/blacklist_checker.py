import logging
import requests

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('blacklist_checker.log'), logging.StreamHandler()]
)

class BlacklistChecker:
    def __init__(self, local_blacklist_path=None, remote_blacklist_url=None):
        self.local_blacklist = self._load_local_blacklist(local_blacklist_path) if local_blacklist_path else set()
        self.remote_blacklist_url = remote_blacklist_url
        logging.info("Initialized BlacklistChecker.")

    def _load_local_blacklist(self, path):
        logging.info(f"Loading local blacklist from {path}.")
        with open(path, 'r') as file:
            return {line.strip() for line in file}

    def _fetch_remote_blacklist(self):
        if not self.remote_blacklist_url:
            return set()
        logging.info(f"Fetching remote blacklist from {self.remote_blacklist_url}.")
        response = requests.get(self.remote_blacklist_url)
        response.raise_for_status()
        return {line.strip() for line in response.text.splitlines()}

    def is_blacklisted(self, url):
        remote_blacklist = self._fetch_remote_blacklist() if self.remote_blacklist_url else set()
        all_blacklisted = self.local_blacklist.union(remote_blacklist)
        is_blacklisted = url in all_blacklisted
        logging.info(f"URL '{url}' is {'blacklisted' if is_blacklisted else 'not blacklisted'}.")
        return is_blacklisted

if __name__ == "__main__":
    checker = BlacklistChecker(local_blacklist_path='blacklist.txt')
    test_url = "http://malicious-site.com"
    print(checker.is_blacklisted(test_url))
