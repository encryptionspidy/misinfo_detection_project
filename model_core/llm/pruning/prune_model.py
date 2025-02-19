import torch
from transformers import AutoModelForSequenceClassification
from torch.nn.utils import prune
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ModelPruner:
    """
    Applies structured pruning techniques to reduce model size and improve inference speed.
    """

    def __init__(self, model_name: str, cache_dir: str = "./model_cache", pruning_amount: float = 0.2):
        """
        Initializes the pruner with the specified model and pruning configuration.

        Args:
            model_name (str): Name of the pre-trained model.
            cache_dir (str): Directory to cache model files.
            pruning_amount (float): Proportion of weights to prune (0 to 1).
        """
        self.model_name = model_name
        self.cache_dir = cache_dir
        self.pruning_amount = pruning_amount
        logging.info(f"Initializing ModelPruner for {model_name} with pruning amount {pruning_amount}")
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name, cache_dir=self.cache_dir)

    def apply_pruning(self):
        """
        Applies global unstructured pruning to reduce model size.
        """
        logging.info("Applying global pruning to model...")
        for name, module in self.model.named_modules():
            if isinstance(module, torch.nn.Linear):
                prune.l1_unstructured(module, name='weight', amount=self.pruning_amount)
        logging.info("Pruning applied successfully.")

    def save_pruned_model(self, output_dir: str = "./pruned_model"):
        """
        Saves the pruned model to the specified directory.

        Args:
            output_dir (str): Directory where the pruned model will be saved.
        """
        logging.info(f"Saving pruned model to {output_dir}...")
        self.model.save_pretrained(output_dir)
        logging.info("Pruned model saved successfully.")


if __name__ == "__main__":
    pruner = ModelPruner("facebook/bart-large-mnli", pruning_amount=0.3)
    pruner.apply_pruning()
    pruner.save_pruned_model()
