"""
ingestionConfig.py
Loads environment variables for the Ingestion Service.
Constructor: no params — loads from env.
"""

import os


class IngestionConfig:

    def __init__(self):
        self.image_directory = os.getenv("IMAGE_DIRECTORY", "/app/images")
        self.bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
        self.kafka_topic_raw = os.getenv("KAFKA_TOPIC_RAW", "raw")
        self.gridfs_service_url = os.getenv("GRIDFS_SERVICE_URL", "http://localhost:8001")

    def validate(self):
        """Check that all required env vars are present."""
        missing = []

        if not self.image_directory:
            missing.append("IMAGE_DIRECTORY")
        if not self.bootstrap_servers:
            missing.append("KAFKA_BOOTSTRAP_SERVERS")
        if not self.kafka_topic_raw:
            missing.append("KAFKA_TOPIC_RAW")
        if not self.gridfs_service_url:
            missing.append("GRIDFS_SERVICE_URL")

        if missing:
            raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")

        if not os.path.isdir(self.image_directory):
            raise FileNotFoundError(f"IMAGE_DIRECTORY does not exist: {self.image_directory}")
