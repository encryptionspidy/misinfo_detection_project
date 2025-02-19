import logging
from pyspark.sql import SparkSession, DataFrame
from delta import configure_spark_with_delta_pip
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('delta_manager.log'), logging.StreamHandler()]
)

class DeltaManager:
    def __init__(self, delta_path: str):
        self.delta_path = delta_path
        self.spark = self._initialize_spark()
        logging.info(f"DeltaManager initialized with Delta path: {self.delta_path}")

    def _initialize_spark(self) -> SparkSession:
        builder = SparkSession.builder \
            .appName("DeltaLakeManager") \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
        
        spark = configure_spark_with_delta_pip(builder).getOrCreate()
        logging.info("Spark session configured with Delta Lake.")
        return spark

    def write_data(self, data: DataFrame, mode: str = 'append'):
        logging.info(f"Writing data to Delta Lake at {self.delta_path} with mode '{mode}'.")
        data.write.format("delta").mode(mode).save(self.delta_path)
        logging.info("Data write completed.")

    def read_data(self, filter_condition: Optional[str] = None) -> DataFrame:
        logging.info(f"Reading data from Delta Lake at {self.delta_path}.")
        df = self.spark.read.format("delta").load(self.delta_path)
        if filter_condition:
            logging.info(f"Applying filter condition: {filter_condition}")
            df = df.filter(filter_condition)
        logging.info("Data read completed.")
        return df

    def update_data(self, condition: str, updates: dict):
        from delta.tables import DeltaTable
        logging.info(f"Updating data in Delta Lake at {self.delta_path}. Condition: {condition}")
        delta_table = DeltaTable.forPath(self.spark, self.delta_path)

        update_expr = ", ".join([f"{key} = '{value}'" for key, value in updates.items()])
        delta_table.update(condition, updates)
        logging.info("Data update completed.")

    def delete_data(self, condition: str):
        from delta.tables import DeltaTable
        logging.info(f"Deleting data from Delta Lake at {self.delta_path} where {condition}.")
        delta_table = DeltaTable.forPath(self.spark, self.delta_path)
        delta_table.delete(condition)
        logging.info("Data deletion completed.")

if __name__ == "__main__":
    manager = DeltaManager(delta_path="/mnt/data/delta/misinformation")
    sample_data = manager.spark.createDataFrame([
        {"id": 1, "text": "Elon Musk founded SpaceX", "verified": True},
        {"id": 2, "text": "The moon is made of cheese", "verified": False}
    ])
    manager.write_data(sample_data, mode='overwrite')

    df = manager.read_data()
    df.show()

    manager.update_data("id = 2", {"verified": "True"})
    manager.delete_data("id = 1")
