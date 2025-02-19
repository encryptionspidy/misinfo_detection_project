import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline
from typing import Any, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('model_loader.log'), logging.StreamHandler()]
)

class ModelLoader:
    """
    Handles loading and configuration of pre-trained language models for misinformation detection.
    """

    def __init__(self, model_name: str, cache_dir: str = "./model_cache"):
        """
        Initializes the ModelLoader with the specified model and tokenizer.
        
        Args:
            model_name (str): Name of the pre-trained model to load.
            cache_dir (str): Directory to cache model files.
        """
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        logging.info(f"ModelLoader initialized with model: {model_name}")
        self._load_model()

    def _load_model(self):
        """
        Loads the model and tokenizer, and initializes the pipeline for sequence classification.
        """
        try:
            logging.info(f"Loading model '{self.model_name}' from Hugging Face...")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, cache_dir=self.cache_dir)
            self.pipeline = pipeline("text-classification", model=self.model, tokenizer=self.tokenizer)
            logging.info(f"Model '{self.model_name}' loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load model '{self.model_name}': {e}")
            raise

    def predict(self, text: str) -> Dict[str, Any]:
        """
        Performs inference on the input text and returns the classification result.

        Args:
            text (str): The input text to classify.

        Returns:
            dict: A dictionary containing labels and confidence scores.
        """
        if not self.pipeline:
            raise RuntimeError("Pipeline is not initialized. Ensure the model is loaded correctly.")
        
        logging.info(f"Performing inference on input text: {text[:50]}...")
        results = self.pipeline(text)
        logging.info(f"Inference completed: {results}")
        return results[0]

    def get_model_info(self) -> Dict[str, str]:
        """
        Returns metadata about the loaded model.

        Returns:
            dict: Model information including model name and tokenizer details.
        """
        return {
            "model_name": self.model_name,
            "tokenizer": self.tokenizer.name_or_path if self.tokenizer else "Not loaded"
        }

if __name__ == "__main__":
    model_loader = ModelLoader("facebook/bart-large-mnli")
    test_text = "The moon is made of green cheese."
    result = model_loader.predict(test_text)
    print(f"Prediction: {result}")
