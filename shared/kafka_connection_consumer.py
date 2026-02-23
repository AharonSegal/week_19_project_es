from confluent_kafka import Consumer
from dotenv import dotenv_values

class KafkaConsumerClient:
    def __init__(self, bootstrap_servers: str, group_id: str):
        self.consumer = Consumer({
            "bootstrap.servers": bootstrap_servers,
            "group.id": group_id,
            "auto.offset.reset": "earliest"
        })

    def subscribe(self, topic: str):
        self.consumer.subscribe([topic])

    def poll(self, timeout: float = 1.0):
        return self.consumer.poll(timeout)

    def close(self):
        self.consumer.close()

# consumer = KafkaConsumerClient(KAFKA_BOOTSTRAP_SERVERS,KAFKA_GROUP_ID_TEXT)

