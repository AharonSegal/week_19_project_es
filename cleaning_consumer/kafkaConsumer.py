"""
gets Raw image event
"""

"""
shared/kafka_consumer.py
Base Kafka consumer connection.
Handles connection only — no business logic.

Usage:
    from shared.kafka_consumer import KafkaConsumerClient

    consumer = KafkaConsumerClient(
        bootstrap_servers="localhost:9092",
        topics=["raw"],
        group_id="my-group",
    )
    consumer.start(callback=my_handler)
"""

from typing import Callable
from confluent_kafka import Consumer, KafkaError


class KafkaConsumerClient:

    def __init__(self, bootstrap_servers: str, topics: list[str], group_id: str):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest",
        })
        self.consumer.subscribe(topics)
        self.topics = topics
        self.running = True

    def start(self, callback: Callable[[str, str | None], None], poll_timeout: float = 1.0):
        """
        Poll messages and pass (topic, value_string) to callback.

        Args:
            callback:     function(topic: str, value: str | None)
            poll_timeout: seconds to wait for a message.
        """
        while self.running:
            msg = self.consumer.poll(poll_timeout)

            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                raise Exception(f"Kafka error: {msg.error()}")

            topic = msg.topic()
            value = msg.value().decode("utf-8") if msg.value() else None
            callback(topic, value)

    def stop(self):
        self.running = False
        self.consumer.close()