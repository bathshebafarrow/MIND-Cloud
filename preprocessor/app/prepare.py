"""
Research code - downloads files from OpenNeuro.
Created on: Wed Mar 22, 2023
@author: Bathsheba Farrow
"""
import app.config as config
import app.aws_client as aws
import logging
import os
import shutil

logger = logging.getLogger()
logger.setLevel(logging.WARN)

# Used to restrict the number of files downloaded from a study to only those being processed
ALLOWED_EXTENSIONS = ['.vhdr', '.vmrk', '.eeg', '.bdf', '.edf', '.set', '.fdt']


def download_study_data(task_id, source_bucket, study_id):
    """
    Used to download data from an entire study
    
    Parameters:
    ----------
    task_id (string): 
        the unique task identifier assigned to the request when created.
    source_bucket (string): 
        the name of the source Amazon S3 bucket from which the data will be retrieved.
    study_id (string): 
        the unique identifier assigned to the study to be downloaded.
    """
    s3_client = None
    if source_bucket == 'openneuro.org':
        s3_client = aws.get_unsigned_client('s3')
    else:
        source_bucket = 'eeg-raw-data'
        s3_client = aws.get_signed_client('s3')
    
    response = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=f'{study_id}/', Delimiter='/')
    if ('Contents' in response):
        for path in response.get('CommonPrefixes'):
            response2 = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=path.get('Prefix'))
            if ('Contents' in response2):
                task_dir = f'tmp/{task_id}/'
                os.makedirs(task_dir, exist_ok=True)
                for file in response2['Contents']:
                    file_name = file['Key']
                    if os.path.splitext(file_name)[1] in ALLOWED_EXTENSIONS:
                        full_name = task_dir + os.path.basename(file_name)
                        s3_client.download_file(source_bucket, 
                                                file_name, 
                                                full_name)
    

def download_study_subject_data(task_id, source_bucket, study_id, subject_id):
    """
    Used to download data for one subject from a study.
    
    Parameters:
    ----------
    task_id (string): 
        the unique task identifier assigned to the request when created.
    source_bucket (string): 
        the name of the source Amazon S3 bucket from which the data will be retrieved.
    study_id (string): 
        the unique identifier assigned to the study to be downloaded.
    subject_id (string): 
        the subject ID from a string (may vary by study).
    """
    task_dir = f'tmp/{task_id}/{subject_id}/'
    os.makedirs(task_dir, exist_ok=True)
    s3_client = None
    if source_bucket == 'openneuro.org':
        s3_client = aws.get_unsigned_client('s3')
    else:
        source_bucket = 'eeg-data-raw'
        s3_client = aws.get_signed_client('s3')
    response = s3_client.list_objects_v2(Bucket=source_bucket, Prefix=f'{study_id}/{subject_id}')
    if ('Contents' in response):
        for file in response['Contents']:
            file_name = file['Key']
            if os.path.splitext(file_name)[1] in ALLOWED_EXTENSIONS:
                full_name = task_dir + os.path.basename(file_name)
                s3_client.download_file(source_bucket, 
                                        file_name, 
                                        full_name)


def upload_data(task_id, subject_id):
    """
    Used to upload processed data for entire study. Compresses the data into a zip file
    before uploading.
    
    Parameters:
    ----------
    task_id (string): 
        the unique task identifier assigned to the request when created.
    """
    source_dir = f'tmp/{task_id}/results/'
    archive_file = f'tmp/{task_id}/{subject_id}_eeg_processed_data'
    shutil.make_archive(archive_file, 'zip', source_dir)
    bucket = config.S3_PREPROCESSED_FILES
    s3_resource_name = f'{task_id}/{subject_id}_eeg_processed_data.zip'
    s3_client = aws.get_signed_client('s3')
    s3_client.upload_file(f'{archive_file}.zip', bucket, s3_resource_name)


def delete_dir(task_id):
    """
    Deletes the directory used to temporarily store data while processing.
    
    Parameters:
    ----------
    task_id (string): 
        the unique task identifier assigned to the request when created.
    """
    task_dir = f'tmp/{task_id}'
    try:
        shutil.rmtree(task_dir)
    except OSError as err:
        logger.error("Could not delete the temporary directory %s: %s: %s", 
                     task_dir,
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])


if __name__=="__main__":
    download_study_subject_data('test212', 'openneuro.org', '', '')
