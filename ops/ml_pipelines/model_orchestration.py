import logging
import yaml
from data_pipeline.stream_ingestion.kafka_processor import KafkaStreamProcessor
from model_core.ensemble.hybrid_detector import HybridDetector
from training_framework.active_learning.active_learner import ActiveLearner
from deployment.triton_models.deploy_misinfo_model import MisinfoModelDeployer
from deployment.monitoring.monitoring_tools import MonitoringTools

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class ModelOrchestrator:
    """
    Orchestrates the end-to-end ML pipeline for misinformation detection.
    """

    def __init__(self, config_path: str):
        """
        Initializes the model orchestrator.

        Args:
            config_path (str): Path to the pipeline configuration YAML file.
        """
        self.config = self.load_config(config_path)
        self.kafka_processor = KafkaStreamProcessor()
        self.detector = HybridDetector()
        self.active_learner = ActiveLearner()
        self.deployer = MisinfoModelDeployer()
        self.monitoring_tools = MonitoringTools()

    @staticmethod
    def load_config(config_path: str):
        """
        Loads the pipeline configuration from YAML.

        Args:
            config_path (str): Path to the config file.

        Returns:
            dict: The loaded configuration.
        """
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        logging.info("Pipeline configuration loaded.")
        return config

    def run_pipeline(self):
        """
        Executes the full ML pipeline: ingestion, training, deployment, and monitoring.
        """
        logging.info("Starting data ingestion...")
        data = self.kafka_processor.consume_messages()

        logging.info("Running hybrid detection model...")
        predictions = self.detector.detect(data)

        if self.config['active_learning']['enable']:
            logging.info("Running active learning loop...")
            self.active_learner.review_predictions(predictions)

        logging.info("Deploying updated model to production...")
        self.deployer.deploy_model(predictions)

        if self.config['deployment']['monitoring']['enable']:
            logging.info("Starting monitoring tools...")
            self.monitoring_tools.monitor_model(predictions)

        logging.info("Pipeline execution complete.")


if __name__ == "__main__":
    orchestrator = ModelOrchestrator(config_path="ops/ml_pipelines/pipeline_config.yaml")
    orchestrator.run_pipeline()
