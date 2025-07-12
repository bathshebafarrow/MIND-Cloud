"""
Author: Bathsheba Jackson
Date Created: 2025-07-11
"""
import json
import pulsar
from models.job import Job
from config import settings

class PulsarProducer:
    """
    Produces messages on the specified Pulsar topic.
    """
    def __init__(self, topic: str):
        self.topic = topic
        self.pulsar_url = f'pulsar://{settings.PULSAR_HOST}:{settings.PULSAR_PORT}'

    def __enter__(self):
        self.client = pulsar.Client(self.pulsar_url)
        self.producer = self.client.create_producer(topic=self.topic)

    def publish_tasks(self, job: Job) -> bool:
        """
        Publishes separate tasks to the Pulsar topic for subject in the job so that multiple 
        workers can process jobs as necessary.

        Parameters
        ----------
        job: Job
            The job that needs to be added to the queue
        
        Returns
        -------
        True if tasks for the job were successfully added; otherwise, returns False. 
        """
        try:
            for subject in job.subjects:
                message = {
                    'job_id': job.id,
                    'source_db': job.source_db,
                    'study_id': job.study_id,
                    'subject_id': subject,
                    'parameters': job.parameters
                }
                json_message = json.dumps(message).encode('utf-8') 
                self.producer.send(json_message)
            return True
        except Exception as ex:
            print(f"Could not publish task for job {job.id}: {ex}")
            return False
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.producer:
            self.producer.close()
        if self.client:
            self.client.close()

def publish_preprocessing_tasks(job: Job) -> bool:
    success = False
    with PulsarProducer(settings.PREPROCESS_TOPIC) as producer:
        success = producer.publish_tasks(job)
    return success
