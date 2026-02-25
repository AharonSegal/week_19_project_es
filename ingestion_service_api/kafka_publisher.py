"""
kafka_publisher.py
Publishes events to a Kafka topic.
Uses shared/kafka_producer.py for the connection.
Constructor: bootstrap_servers, topic_name, logger
 Gets logger from main 
"""

from logging import Logger
import json

from shared.kafka_producer import KafkaProducerClient


class KafkaPublisher:

    def __init__(self, bootstrap_servers: str, topic_name: str, logger: Logger):
        self.producer = KafkaProducerClient(bootstrap_servers)
        self.topic_name = topic_name

        self.logger = logger
        self.logger.info("KafkaPublisher ready — topic: %s", topic_name)


    def publish(self, event: dict) -> None:
        """
        Publish an event dict to the Kafka topic.

        Args:
            event: dict containing image_id, raw_text, metadata, etc.
        """
        image_id = event.get("image_id", "unknown")
        self.logger.info("Publishing event for image_id=%s to %s", image_id, self.topic_name)

        try:
            self.producer.send(
                topic=self.topic_name,
                key=image_id,
                value=json.dumps(event).encode("utf-8"),
            )
            self.producer.flush()
            self.logger.info("Published image_id=%s", image_id)

        except Exception as e:
            self.logger.error("Failed to publish event: %s", e)
            raise

