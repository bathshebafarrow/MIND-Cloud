import logging
import uuid
import application 
from botocore.exceptions import ClientError
from collections import OrderedDict
from datetime import datetime

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def create_task(user_name, bucket_name, study_id, subjects, params):
    db = application.get_db_client()
    table = db.Table('FileProcessingTask')
    task_id = uuid.uuid4().hex
    try:
        response = table.put_item(
            Item = { 
                'TaskId': task_id,
                'CreatedDate': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
                'UserName': user_name,
                'SourceDB': bucket_name,
                'StudyId': study_id,
                'SubjectId': subjects,
                'Subjects': len(subjects),
                'TotalProcessed': 0,
                'Parameters': params,
                'TaskStatus': 'Pending'
            }
        )
        print(response)
        return task_id
    except ClientError as err:
        logger.error("Could not retrieve the record: %s: %s", 
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])
        return None

def retreive_task(task_id):
    try:
        db = application.get_db_client()
        table = db.Table('FileProcessingTask')
        response = table.get_item(Key={'TaskId': task_id})
        return response['Item']
    except ClientError as err:
        logger.error("Could not retrieve the record: %s: %s", 
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])
        return None

def retreive_all_tasks():
    try:
        db = application.get_db_client()
        table = db.Table('FileProcessingTask')
        response = table.scan()
        return response['Items']
    except ClientError as err:
        logger.error("Could not retrieve the records: %s: %s", 
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])
        return []
        
def update_task_status(task_id, task_status):
    try:
        db = application.get_db_client()
        table = db.Table('FileProcessingTask')
        response = table.update_item(
            Key={'TaskId':task_id},
            UpdateExpression = 'SET TaskStatus=:s',
            ExpressionAttributeValues = {
                ':s': task_status
            },
            ReturnValues='UPDATED_NEW'
        )
        return(response)
    except ClientError as err:
        logger.error("Could not retrieve the record: %s: %s", 
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])
        return None
        
def delete_task(task_id):
    try:
        db = application.get_db_client()
        table = db.Table('FileProcessingTask')
        response = table.delete_item(
            Key={'TaskId':task_id}
        )
        return(response)
    except ClientError as err:
        logger.error("Could not retrieve the record: %s: %s", 
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])
        return None
    
def get_subject_list(bucket, study_id):
    s3_client = None
    if bucket == application.get_external_bucket():
        s3_client = application.get_s3_client()
    else:
        bucket = application.get_internal_bucket()
        s3_client = application.get_s3_client()
    paginator = s3_client.get_paginator("list_objects_v2")
    subjects = OrderedDict([])
    for pages in paginator.paginate(Bucket=bucket, Prefix=study_id):
        # Inside of each page, return the common prefixes (folders) first
        for page in pages.get("Contents", []):
            sub = page['Key'].split('/')[1]
            if sub.startswith("sub"):
                subjects[sub] = sub
    options = []
    for subject in subjects:
        options.append({'id':subject, 'name':subject})
    return options

if __name__ == '__main__':
    tasks = retreive_all_tasks()
    for task in tasks:
        print(task)
