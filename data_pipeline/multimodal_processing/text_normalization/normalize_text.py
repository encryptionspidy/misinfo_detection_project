import re
import logging
import spacy
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('normalize_text.log'), logging.StreamHandler()]
)

class TextNormalizer:
    def __init__(self, language='en'):
        self.language = language
        self.stop_words = set(stopwords.words(language))
        self.nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
        logging.info("Initialized TextNormalizer.")

    def normalize(self, text):
        logging.info(f"Normalizing text: {text[:50]}...")
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\w\s]', '', text)
        
        tokens = word_tokenize(text)
        filtered_tokens = [word for word in tokens if word not in self.stop_words]

        lemmatized_tokens = [token.lemma_ for token in self.nlp(" ".join(filtered_tokens))]
        normalized_text = ' '.join(lemmatized_tokens)
        logging.info("Text normalization complete.")
        return normalized_text

if __name__ == "__main__":
    normalizer = TextNormalizer()
    sample_text = "Breaking News! This is an example of misinformation spreading rapidly."
    print(normalizer.normalize(sample_text))
