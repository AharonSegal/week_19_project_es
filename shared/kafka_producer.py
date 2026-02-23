"""
shared/kafka_producer.py
Base Kafka producer connection.
Handles connection only — no business logic.

Usage:
    from shared.kafka_producer import KafkaProducerClient

    producer = KafkaProducerClient(bootstrap_servers="localhost:9092")
    producer.send(topic="raw", value=b'{"key": "value"}')
    producer.flush()
"""

from confluent_kafka import Producer


class KafkaProducerClient:

    def __init__(self, bootstrap_servers: str):
        self.producer = Producer({"bootstrap.servers": bootstrap_servers})

    def send(self, topic: str, key: str | None = None, value: bytes = b""):
        self.producer.produce(topic=topic, key=key, value=value)

    def flush(self):
        self.producer.flush()