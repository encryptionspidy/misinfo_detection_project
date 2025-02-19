import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class HumanReview:
    """
    Human-in-the-loop system for reviewing uncertain predictions.
    """

    def __init__(self):
        self.review_queue = []

    def add_to_review(self, sample_id: str, data: Dict):
        """
        Adds a data sample to the human review queue.

        Args:
            sample_id (str): Unique identifier for the data sample.
            data (Dict): The data and associated metadata to be reviewed.
        """
        self.review_queue.append({'id': sample_id, 'data': data})
        logging.info(f"Sample {sample_id} added to human review queue.")

    def perform_review(self) -> List[Dict]:
        """
        Simulates human review process.

        Returns:
            List[Dict]: Reviewed data with final decisions.
        """
        reviewed_data = []
        for item in self.review_queue:
            # Simulate human decision (replace with actual human interaction in production)
            decision = {"label": "misinformation" if hash(item['id']) % 2 == 0 else "truth"}
            item['decision'] = decision
            reviewed_data.append(item)
            logging.info(f"Sample {item['id']} reviewed and labeled as {decision['label']}.")

        self.review_queue.clear()
        return reviewed_data


if __name__ == "__main__":
    review_system = HumanReview()
    review_system.add_to_review("sample_001", {"text": "This is a potentially false claim."})
    review_system.add_to_review("sample_002", {"text": "Breaking news with unverified sources."})

    final_decisions = review_system.perform_review()
    logging.info(f"Final reviewed data: {final_decisions}")
