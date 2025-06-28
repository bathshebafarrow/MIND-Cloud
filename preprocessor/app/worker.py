import app.aws_client as aws
from app.prepare import delete_dir, download_study_subject_data, upload_data
from app.preprocess import preprocess_subject_data
from datetime import datetime
import json
import logging

logger = logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

class FileQueueWorker:

    def __init__(self, queue_url):
        self.name = 'FileProcessor'
        self.queue_url = queue_url

    def __enter__(self):
        self.sqs_client = aws.get_signed_client('sqs')
        self.db_client = aws.get_db_client()

    def process_queue(self):
        while True:
            try:
                response = self.sqs_client.receive_message(
                    QueueUrl=self.queue_url,
                    AttributeNames=[
                        'SentTimestamp'
                    ],
                    MaxNumberOfMessages=1,
                    MessageAttributeNames=[
                        'All'
                    ],
                    VisibilityTimeout=5,
                    WaitTimeSeconds=20
                )

                # Process message if found
                if 'Messages' in response:
                    message = response['Messages'][0]
                    receipt_handle = message['ReceiptHandle']
                    data = json.loads(message['Body'])

                    # Delete the message fromn the queue
                    self.sqs_client.delete_message(
                        QueueUrl=self.queue_url,
                        ReceiptHandle=receipt_handle
                    )

                    self.process_message(data)
            except KeyboardInterrupt:
                return    
            except Exception as ex:
                print(f'Error occurred during processing: {ex}')

    def process_message(self, user_data) -> bool:
        """
        Process the user data.
        user_data (json): user parameter selections in json format.
        """
        task_id = None
        success = False
        try:
            task_id = user_data.get("task_id")
            self.update_task_status(task_id, "Processing")
            bucket = user_data.get("bucket")
            study = user_data.get("study")
            subject_id = user_data.get("subject").get("S")
            logger.info(subject_id)
            params = user_data.get("params")
            download_study_subject_data(task_id, bucket, study, subject_id)
            preprocess_subject_data(task_id, subject_id, params)
            upload_data(task_id, subject_id)
            logger.info(f'Processed {subject_id} for {task_id}')
            self.update_task_status(task_id, "Processing")
            success = True
        except Exception as ex:
            logger.error("Could not complete processing for task %s: %s", task_id, ex)
            self.update_task_status(task_id, "Error")
        if task_id is not None:
            delete_dir(task_id)
        return success

    def update_task_status(self, task_id, task_status) -> None:
        """
        Update the status of the task in the database.
        task_id (string): the unique identifier assigned to the file processing request.
        task_status (string): the current status of the file processing.
        """
        try:
            table = self.db_client.Table('FileProcessingTask')
            table.update_item(
                Key={'TaskId':task_id},
                UpdateExpression='SET TaskStatus=:s1, StatusDate = :s2',
                ExpressionAttributeValues = {
                    ':s1': task_status,
                    ':s2': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
                },
                ReturnValues='NONE'
            )
        except Exception as ex:
            logger.error("Could not update the status for task %s: %s", task_id, ex)
   
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f'Exiting {self.name}')
        self.sqs_client.close()
        self.db_client.close()
