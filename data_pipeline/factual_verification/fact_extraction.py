import logging
import spacy
from typing import List, Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('fact_extraction.log'), logging.StreamHandler()]
)

class FactExtractor:
    def __init__(self, model: str = "en_core_web_sm"):
        self.nlp = spacy.load(model)
        logging.info("Initialized FactExtractor with SpaCy model.")

    def extract_facts(self, text: str) -> List[Dict[str, str]]:
        logging.info("Extracting facts from input text.")
        doc = self.nlp(text)
        facts = []

        for sent in doc.sents:
            subject, verb, obj = self._extract_subject_verb_object(sent)
            if subject and verb and obj:
                fact = {
                    "subject": subject,
                    "predicate": verb,
                    "object": obj
                }
                facts.append(fact)
                logging.debug(f"Extracted fact: {fact}")

        logging.info(f"Total facts extracted: {len(facts)}")
        return facts

    def _extract_subject_verb_object(self, sentence) -> (str, str, str):
        subject, verb, obj = "", "", ""
        for token in sentence:
            if "subj" in token.dep_:
                subject = token.text
            elif "obj" in token.dep_:
                obj = token.text
            elif token.pos_ == "VERB":
                verb = token.lemma_
        return subject, verb, obj

if __name__ == "__main__":
    extractor = FactExtractor()
    text = "Elon Musk founded SpaceX. The company launched its first rocket in 2008."
    facts = extractor.extract_facts(text)
    print(facts)
