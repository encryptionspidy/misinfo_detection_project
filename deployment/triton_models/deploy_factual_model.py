import os
import logging
import tritonclient.http as httpclient
from tritonclient.utils import InferenceServerException

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MisinfoModelDeployer:
    """
    Deploys the misinformation detection model using Triton Inference Server.
    """

    def __init__(self, model_name='misinfo_detector', triton_url='localhost:8000', model_repo_path='/models/misinfo'):
        """
        Initializes the model deployer.

        Args:
            model_name (str): Name of the model.
            triton_url (str): URL of the Triton Inference Server.
            model_repo_path (str): Path to the model repository.
        """
        self.model_name = model_name
        self.triton_url = triton_url
        self.model_repo_path = model_repo_path
        self.client = httpclient.InferenceServerClient(url=self.triton_url)

    def check_server_status(self):
        """
        Checks if the Triton server is live and ready.
        """
        try:
            if self.client.is_server_live():
                logging.info("Triton Server is live.")
            if self.client.is_server_ready():
                logging.info("Triton Server is ready to accept models.")
        except InferenceServerException as e:
            logging.error(f"Triton Server Error: {e}")
            raise

    def deploy_model(self):
        """
        Deploys the misinformation model to Triton Inference Server.
        """
        self.check_server_status()
        model_path = os.path.join(self.model_repo_path, self.model_name)
        
        if not os.path.exists(model_path):
            logging.error(f"Model path {model_path} does not exist. Ensure the model is exported correctly.")
            return

        try:
            self.client.load_model(self.model_name)
            logging.info(f"Model {self.model_name} successfully deployed on Triton Server.")
        except InferenceServerException as e:
            logging.error(f"Error deploying model {self.model_name}: {e}")
            raise

    def get_model_metadata(self):
        """
        Retrieves the deployed model's metadata.
        """
        try:
            metadata = self.client.get_model_metadata(self.model_name)
            logging.info(f"Model Metadata: {metadata}")
            return metadata
        except InferenceServerException as e:
            logging.error(f"Failed to retrieve model metadata: {e}")
            raise


if __name__ == "__main__":
    deployer = MisinfoModelDeployer()
    deployer.deploy_model()
    deployer.get_model_metadata()
