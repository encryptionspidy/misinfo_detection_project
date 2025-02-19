import logging
from model_core.llm.base_model.model_loader import LLMModelLoader
from model_core.graph_networks.graph_neural_network import GraphNeuralNetwork
from model_core.malicious_url_model.malicious_url_model import MaliciousURLModel
import torch
import torch.nn.functional as F

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HybridDetector:
    """
    A hybrid misinformation detection framework that combines LLMs, GNNs, and URL detection for enhanced accuracy.
    """

    def __init__(self, llm_model_name: str, gnn_config: dict):
        """
        Initializes the hybrid detection framework with LLM, GNN, and URL models.

        Args:
            llm_model_name (str): Name of the pre-trained language model for textual analysis.
            gnn_config (dict): Configuration for Graph Neural Network (input_dim, hidden_dim, output_dim).
        """
        logging.info("Initializing Hybrid Detector...")
        self.llm_model = LLMModelLoader(llm_model_name).load_model()
        self.gnn_model = GraphNeuralNetwork(**gnn_config)
        self.url_model = MaliciousURLModel().load_model()

    def detect(self, text_input: str, graph_data, url_list: list):
        """
        Performs hybrid detection by aggregating outputs from LLM, GNN, and URL models.

        Args:
            text_input (str): Input text for LLM classification.
            graph_data: Graph data for GNN-based misinformation propagation analysis.
            url_list (list): List of URLs for malicious content detection.

        Returns:
            dict: Combined prediction results.
        """
        llm_result = self._analyze_text(text_input)
        gnn_result = self._analyze_graph(graph_data)
        url_result = self._check_urls(url_list)

        combined_score = (llm_result["score"] + gnn_result["score"] + url_result["score"]) / 3
        final_decision = combined_score > 0.5

        return {
            "llm_result": llm_result,
            "gnn_result": gnn_result,
            "url_result": url_result,
            "combined_score": combined_score,
            "misinformation_detected": final_decision
        }

    def _analyze_text(self, text_input: str):
        """
        Analyzes text using the LLM model.

        Args:
            text_input (str): Input text.

        Returns:
            dict: LLM classification output.
        """
        logging.info("Analyzing text with LLM...")
        inputs = self.llm_model.tokenizer(text_input, return_tensors="pt")
        outputs = self.llm_model.model(**inputs)
        score = torch.softmax(outputs.logits, dim=1)[0][1].item()

        return {"score": score, "classification": "misinformation" if score > 0.5 else "legitimate"}

    def _analyze_graph(self, graph_data):
        """
        Analyzes graph data using the GNN model.

        Args:
            graph_data: Graph structure.

        Returns:
            dict: GNN output indicating propagation anomalies.
        """
        logging.info("Analyzing graph structure with GNN...")
        self.gnn_model.eval()
        with torch.no_grad():
            output = self.gnn_model(graph_data)
            score = F.softmax(output, dim=1)[0][1].item()

        return {"score": score, "propagation_anomaly": score > 0.5}

    def _check_urls(self, url_list: list):
        """
        Checks URLs for malicious content using the URL detection model.

        Args:
            url_list (list): List of URLs.

        Returns:
            dict: URL analysis result.
        """
        logging.info("Checking URLs for malicious content...")
        malicious_count = sum([self.url_model.predict(url) for url in url_list])
        score = malicious_count / len(url_list) if url_list else 0

        return {"score": score, "malicious_urls_found": malicious_count}


if __name__ == "__main__":
    detector = HybridDetector("microsoft/deberta-v3-base", {"input_dim": 2, "hidden_dim": 4, "output_dim": 2})
    results = detector.detect(
        "Breaking news: Aliens have landed!",
        graph_data=None,  # Placeholder for graph data
        url_list=["http://malicious-site.com", "http://safe-site.org"]
    )
    print(results)
