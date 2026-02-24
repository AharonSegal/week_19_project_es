"""
gets from kafka
passes to be processed 
publishes to kafka
"""

# for local run 
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from clean_config import CleanConfig

from shared.kafka_connection_consumer import KafkaConsumerClient
from shared.kafka_producer import KafkaProducerClient
from shared.logger import get_logger


class cleanOrchestrator():
    def __init__(self):
        self.config = CleanConfig()
        self.kafka_consumer = KafkaConsumerClient(self.config.bootstrap_servers,self.config.clean_group)
        self.kafka_publisher = KafkaProducerClient(self.config.bootstrap_servers)
        self.logger = get_logger("cleaning_consumer")

    def text_cleaner(self):
        pass

    def kafka_publish(self):
        pass

    def clean(self):
        while True:
            image = self.kafka_consumer.consumer.poll(1.0)
            if image is None:
                continue

            
    
