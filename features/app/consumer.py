"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
import pulsar
from config import settings

class TaskConsumer:
    def __init__(self, resource):
        self.pulsar_url = f'pulsar://{settings.PULSAR_HOST}:{settings.PULSAR_PORT}'

    def __enter__(self):
        self.client = pulsar.Client(self.pulsar_url)
        self.consumer = self.client.subscribe(
            topic=settings.PULSAR_TOPIC,
            subscription_name=settings.PULSAR_SUBSCRIPTION,
            subscription_type=pulsar.ConsumerType.Exclusive # For now
        )

    def process_tasks(self):
        while True:
            msg = self.consumer.receive()
            # Add logic to process messages
            
    def __exit__(self, exc_type, exc_value, traceback):
        if self.consumer:
            self.consumer.close()
        if self.client:
            self.client.close()