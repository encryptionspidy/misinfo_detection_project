import json
import logging
from kafka import KafkaConsumer, KafkaProducer
from kafka.errors import KafkaError
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler("kafka_processor.log"), logging.StreamHandler()]
)
logger = logging.getLogger("KafkaProcessor")

class KafkaProcessor:
    def __init__(self, config):
        """
        Initialize Kafka consumer and producer.
        :param config: Dictionary containing Kafka configurations.
        """
        self.consumer = KafkaConsumer(
            config['input_topic'],
            bootstrap_servers=config['bootstrap_servers'],
            auto_offset_reset='earliest',
            enable_auto_commit=True,
            group_id=config['group_id'],
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

        self.producer = KafkaProducer(
            bootstrap_servers=config['bootstrap_servers'],
            value_serializer=lambda x: json.dumps(x).encode('utf-8')
        )

        self.output_topic = config['output_topic']
        self.max_workers = config.get('max_workers', 5)
        logger.info("Kafka Processor initialized successfully.")

    def process_message(self, message):
        """
        Process incoming message and return processed data.
        Override this method based on specific processing logic.
        :param message: The message payload from Kafka.
        :return: Processed data.
        """
        try:
            logger.debug(f"Processing message: {message}")
            # Placeholder for processing logic
            # Example: Simple data enrichment
            processed_data = {
                "original": message,
                "processed_at": self._get_timestamp(),
                "status": "processed"
            }
            return processed_data
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            return None

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.utcnow().isoformat()

    def send_to_output_topic(self, data):
        """
        Send processed data to the output Kafka topic.
        :param data: Data to send.
        """
        try:
            self.producer.send(self.output_topic, value=data)
            self.producer.flush()
            logger.info(f"Data sent to output topic: {self.output_topic}")
        except KafkaError as e:
            logger.error(f"Failed to send data to Kafka: {e}")

    def run(self):
        """
        Start consuming and processing messages from the Kafka topic.
        """
        logger.info(f"Starting Kafka consumer on topic: {self.consumer.subscription()}")
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for message in self.consumer:
                logger.info(f"Received message: {message.value}")
                executor.submit(self._process_and_send, message.value)

    def _process_and_send(self, message):
        """
        Internal helper to process and send data in parallel.
        :param message: Message payload to process.
        """
        processed_data = self.process_message(message)
        if processed_data:
            self.send_to_output_topic(processed_data)

if __name__ == "__main__":
    CONFIG = {
        "bootstrap_servers": ["localhost:9092"],
        "input_topic": "raw_misinfo_stream",
        "output_topic": "processed_misinfo_stream",
        "group_id": "misinfo_processor_group",
        "max_workers": 10
    }

    processor = KafkaProcessor(CONFIG)
    processor.run()
