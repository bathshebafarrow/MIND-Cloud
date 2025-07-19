"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
import json
import pulsar
import requests
from models import Job, JobUpdate
from config import settings
from prepare import archive_results, download_study_data
from preprocess import preprocess_subject

class JobConsumer:
    def __init__(self):
        self.pulsar_url = settings.PULSAR_URL

    def __enter__(self):
        self.client = pulsar.Client(self.pulsar_url)
        self.consumer = self.client.subscribe(
            topic=settings.PULSAR_TOPIC,
            subscription_name=settings.PULSAR_SUBSCRIPTION,
            subscription_type=pulsar.ConsumerType.Shared
        )

    def process_messages(self):
        """
        Processes messages on the Pulsar topic.
        """
        while True:
            message = self.consumer.receive()
            try:
                data = message.data().decode('utf-8')
                job = Job(**json.loads(data))
                job_dir = download_study_data(job)
                preprocess_subject(job, job_dir)
                archive_results(job)
                self.update_job(job, "PROCESSED")
                self.consumer.acknowledge(message)
            except Exception as ex:
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