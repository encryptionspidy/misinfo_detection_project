import logging
from typing import List, Dict
from collections import Counter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('factual_consistency_analyzer.log'), logging.StreamHandler()]
)

class FactualConsistencyAnalyzer:
    def __init__(self):
        logging.info("Initialized FactualConsistencyAnalyzer.")

    def analyze_consistency(self, fact_sets: List[List[Dict[str, str]]]) -> List[Dict[str, str]]:
        logging.info("Analyzing factual consistency across sources.")
        fact_counter = Counter()

        for source_facts in fact_sets:
            for fact in source_facts:
                fact_key = f"{fact['subject']}|{fact['predicate']}|{fact['object']}"
                fact_counter[fact_key] += 1

        total_sources = len(fact_sets)
        consistent_facts = [
            {'fact': fact, 'consistency_score': count / total_sources}
            for fact, count in fact_counter.items()
            if count > 1
        ]

        logging.info(f"Identified {len(consistent_facts)} consistent facts across sources.")
        return consistent_facts

if __name__ == "__main__":
    analyzer = FactualConsistencyAnalyzer()
    source1 = [{"subject": "Elon Musk", "predicate": "found", "object": "SpaceX"}]
    source2 = [{"subject": "Elon Musk", "predicate": "found", "object": "SpaceX"},
               {"subject": "NASA", "predicate": "launch", "object": "Falcon 9"}]
    consistency = analyzer.analyze_consistency([source1, source2])
    print(consistency)
