import logging
from typing import List, Dict
import sqlite3

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('knowledge_base_matcher.log'), logging.StreamHandler()]
)

class KnowledgeBaseMatcher:
    def __init__(self, db_path: str = 'knowledge_base.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        logging.info("Initialized KnowledgeBaseMatcher with database.")

    def match_facts(self, facts: List[Dict[str, str]]) -> List[Dict[str, str]]:
        logging.info("Matching extracted facts with the knowledge base.")
        results = []

        for fact in facts:
            query = f"""
            SELECT * FROM facts
            WHERE subject = ? AND predicate = ? AND object = ?
            """
            self.cursor.execute(query, (fact['subject'], fact['predicate'], fact['object']))
            match = self.cursor.fetchone()
            result = {
                'fact': fact,
                'match_found': bool(match)
            }
            results.append(result)
            logging.debug(f"Fact: {fact}, Match Found: {bool(match)}")

        logging.info(f"Total facts matched: {sum(r['match_found'] for r in results)}")
        return results

if __name__ == "__main__":
    matcher = KnowledgeBaseMatcher()
    facts = [
        {"subject": "Elon Musk", "predicate": "found", "object": "SpaceX"},
        {"subject": "NASA", "predicate": "launch", "object": "Falcon 9"}
    ]
    matches = matcher.match_facts(facts)
    print(matches)
