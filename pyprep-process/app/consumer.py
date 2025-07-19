"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
import json
import requests
from config import settings
from models import Job, JobUpdate
from prepare import cleanup_files, prepare_study_data
from preprocess import preprocess_subject
from pulsar import Client, Consumer, ConsumerType

class JobConsumer:
    client: Client
    consumer: Consumer
    
    def __init__(self):
        self.topic = settings.PULSAR_TOPIC

    def __enter__(self):
        self.client = Client(settings.PULSAR_URL)
        self.consumer = self.client.subscribe(
            topic=self.topic,
            subscription_name=settings.PULSAR_SUBSCRIPTION,
            subscription_type=ConsumerType.Shared
        )
        return self

    def process_messages(self):
        """
        Processes messages on the Pulsar topic.
        """
        while True:
            try:
                message = self.consumer.receive()
                data = message.data().decode('utf-8')
                job = Job(**json.loads(data))
                input_dir, output_dir = prepare_study_data(job)
                preprocess_subject(job, input_dir, output_dir)
                cleanup_files(input_dir)

                self.update_job(job, "PROCESSED")
                self.consumer.acknowledge(message)
            except Exception as ex:
                print(ex)
                self.update_job(job, "ERROR")
                self.consumer.negative_acknowledge(message)

    def update_job(self, job: Job, status: str):
        try:
            job_update = JobUpdate(
                id = job.id,
                status = status
            )
            response = requests.post(settings.JOB_UPDATE_URL, json=job_update)
            if response.status_code == 200: 
                return True
            return False
        except Exception as ex:
            print(f'Could not update the status for job {job.id}: {ex}')

    def __exit__(self, exc_type, exc_value, traceback):
        if self.consumer:
            self.consumer.close()
        if self.client:
            self.client.close()