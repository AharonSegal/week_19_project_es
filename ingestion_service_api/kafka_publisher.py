"""
kafka_publisher.py
Publishes events to a Kafka topic.
Constructor: bootstrap_servers, topic_name, logger
"""

import json
from logging import Logger

from confluent_kafka import Producer


class KafkaPublisher:

    def __init__(self, bootstrap_servers: str, topic_name: str, logger: Logger):
        self.topic_name = topic_name
        self.logger = logger
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})
        self.logger.info(
            "KafkaPublisher ready — topic: %s, servers: %s",
            topic_name, bootstrap_servers,
        )

    def _delivery_callback(self, err, msg):
        if err:
            self.logger.error("Kafka delivery failed: %s", err)
        else:
            self.logger.info(
                "Published to %s [partition %s] offset %s",
                msg.topic(), msg.partition(), msg.offset(),
            )

    def publish(self, event: dict) -> None:
        """
        Publish an event dict to the Kafka topic.

        Args:
            event: dict containing image_id, raw_text, metadata, etc.
        """
        image_id = event.get("image_id", "unknown")
        self.logger.info("Publishing event for image_id=%s to %s", image_id, self.topic_name)

        try:
            self.producer.produce(
                topic=self.topic_name,
                key=image_id,
                value=json.dumps(event),
                callback=self._delivery_callback,
            )
            self.producer.flush()

        except Exception as e:
            self.logger.error("Failed to publish event: %s", e)
            raise
