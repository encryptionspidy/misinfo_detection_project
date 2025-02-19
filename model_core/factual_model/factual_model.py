import logging
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class FactualVerificationModel:
    """
    A factual verification model using a transformer-based architecture like FLAN-T5 or Falcon.
    """

    def __init__(self, model_name="google/flan-t5-large"):
        """
        Initializes the factual verification model.

        Args:
            model_name (str): The Hugging Face model name to use for factual verification.
        """
        logging.info(f"Loading factual verification model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    def verify_claim(self, claim: str, context: str):
        """
        Verifies the factual accuracy of a claim given supporting context.

        Args:
            claim (str): The claim to verify.
            context (str): The supporting context.

        Returns:
            str: The model's assessment of the claim (e.g., "true", "false", "unsupported").
        """
        input_text = f"Claim: {claim} \n Context: {context} \n Answer:"
        inputs = self.tokenizer(input_text, return_tensors="pt")
        output = self.model.generate(**inputs)
        answer = self.tokenizer.decode(output[0], skip_special_tokens=True)

        return answer


if __name__ == "__main__":
    model = FactualVerificationModel()
    claim = "The Eiffel Tower is in Berlin."
    context = "The Eiffel Tower is a landmark located in Paris, France."
    result = model.verify_claim(claim, context)
    print(f"Verification Result: {result}")
