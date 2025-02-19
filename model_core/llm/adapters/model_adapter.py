import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelAdapter:
    """
    Adapts pre-trained models with task-specific configurations for enhanced performance.
    """

    def __init__(self, model_name: str, num_labels: int, cache_dir: str = "./model_cache"):
        """
        Initializes the model adapter with the specified model and configuration.

        Args:
            model_name (str): The pre-trained model name.
            num_labels (int): The number of output labels for classification.
            cache_dir (str): Directory to cache the model files.
        """
        self.model_name = model_name
        self.num_labels = num_labels
        self.cache_dir = cache_dir
        self.model = None
        self.tokenizer = None
        logging.info(f"Initializing ModelAdapter for model: {model_name}")
        self._load_and_adapt_model()

    def _load_and_adapt_model(self):
        """
        Loads the base model and adapts it for the specified classification task.
        """
        try:
            logging.info("Loading tokenizer and model for adaptation...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            self.model = AutoModelForSequenceClassification.from_pretrained(
                self.model_name, num_labels=self.num_labels, cache_dir=self.cache_dir
            )
            logging.info(f"Model '{self.model_name}' adapted for {self.num_labels}-label classification.")
        except Exception as e:
            logging.error(f"Error in model adaptation: {e}")
            raise

    def get_model_and_tokenizer(self):
        """
        Returns the adapted model and tokenizer.

        Returns:
            tuple: (model, tokenizer)
        """
        return self.model, self.tokenizer


if __name__ == "__main__":
    adapter = ModelAdapter("microsoft/deberta-v3-base", num_labels=3)
    model, tokenizer = adapter.get_model_and_tokenizer()
    print(f"Model adapted: {model.config}")
