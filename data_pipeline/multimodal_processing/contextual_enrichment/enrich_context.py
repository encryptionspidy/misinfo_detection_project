from SPARQLWrapper import SPARQLWrapper, JSON
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('enrich_context.log'), logging.StreamHandler()]
)

class ContextualEnricher:
    def __init__(self, endpoint_url="https://dbpedia.org/sparql"):
        self.sparql = SPARQLWrapper(endpoint_url)
        logging.info("Initialized ContextualEnricher.")

    def enrich_with_knowledge_graph(self, entity):
        logging.info(f"Fetching context for entity: {entity}")
        query = f"""
        SELECT ?abstract WHERE {{
          dbr:{entity} dbo:abstract ?abstract .
          FILTER (lang(?abstract) = 'en')
        }} LIMIT 1
        """
        self.sparql.setQuery(query)
        self.sparql.setReturnFormat(JSON)

        try:
            results = self.sparql.query().convert()
            abstract = results["results"]["bindings"][0]["abstract"]["value"] if results["results"]["bindings"] else "No information available."
            logging.info(f"Fetched abstract: {abstract[:50]}...")
            return abstract
        except Exception as e:
            logging.error(f"SPARQL query failed: {e}")
            return "Contextual information not available."

if __name__ == "__main__":
    enricher = ContextualEnricher()
    entity_context = enricher.enrich_with_knowledge_graph("Misinformation")
    print(entity_context)
