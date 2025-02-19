import prometheus_client
from prometheus_client import Gauge, Counter, start_http_server
import logging
import time
import requests

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define Prometheus metrics
INFERENCE_LATENCY = Gauge('inference_latency_seconds', 'Time taken for inference')
INFERENCE_ERRORS = Counter('inference_errors_total', 'Total number of inference errors')
MODEL_DRIFT_DETECTED = Counter('model_drift_detected_total', 'Total number of drift detections')
GPU_UTILIZATION = Gauge('gpu_utilization_percent', 'GPU utilization percentage')
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')


class MonitoringTool:
    """
    Monitoring tool for Triton Inference Server and deployed models.
    """

    def __init__(self, triton_url='http://localhost:8002/metrics'):
        self.triton_url = triton_url

    def fetch_metrics(self):
        """
        Fetches metrics from the Triton Inference Server.
        """
        try:
            response = requests.get(self.triton_url)
            if response.status_code == 200:
                logging.info("Successfully fetched Triton metrics.")
            else:
                logging.error(f"Failed to fetch metrics: {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Error fetching metrics: {e}")

    def simulate_inference(self):
        """
        Simulates inference calls to generate monitoring data.
        """
        try:
            start_time = time.time()
            # Simulate inference delay
            time.sleep(0.2)
            latency = time.time() - start_time
            INFERENCE_LATENCY.set(latency)
            logging.info(f"Inference latency recorded: {latency:.4f} seconds")
        except Exception as e:
            INFERENCE_ERRORS.inc()
            logging.error(f"Inference error occurred: {e}")

    def monitor_resources(self):
        """
        Monitors system resources like GPU utilization and memory usage.
        """
        import psutil
        try:
            memory_info = psutil.virtual_memory()
            MEMORY_USAGE.set(memory_info.used)
            logging.info(f"Memory usage recorded: {memory_info.used} bytes")
            
            # Placeholder GPU Utilization (use NVIDIA tools for real GPU monitoring)
            gpu_utilization = 70  # Simulated GPU load percentage
            GPU_UTILIZATION.set(gpu_utilization)
            logging.info(f"GPU utilization recorded: {gpu_utilization}%")
        except Exception as e:
            logging.error(f"Resource monitoring error: {e}")

    def detect_drift(self):
        """
        Placeholder for drift detection monitoring.
        """
        import random
        drift_detected = random.choice([True, False])
        if drift_detected:
            MODEL_DRIFT_DETECTED.inc()
            logging.warning("Model drift detected!")

    def run(self):
        """
        Starts the monitoring server and continuously records metrics.
        """
        start_http_server(8003)  # Expose custom Prometheus metrics
        logging.info("Monitoring server started at http://localhost:8003")

        while True:
            self.fetch_metrics()
            self.simulate_inference()
            self.monitor_resources()
            self.detect_drift()
            time.sleep(10)


if __name__ == "__main__":
    monitor = MonitoringTool()
    monitor.run()
