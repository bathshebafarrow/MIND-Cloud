"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
import json
import pulsar
from config import settings

class JobConsumer:
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
            message = self.consumer.receive()
            json_object = json.loads(message.data().decode('utf-8'))
            self.consumer.acknowledge(message)

    def __exit__(self, exc_type, exc_value, traceback):
        if self.consumer:
            self.consumer.close()
        if self.client:
            self.client.close()