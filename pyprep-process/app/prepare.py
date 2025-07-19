"""
Research code - downloads files from OpenNeuro.
Created on: Wed Mar 22, 2023
@author: Bathsheba Farrow
"""
import boto3
import logging
import os
import shutil
from botocore import UNSIGNED
from botocore.config import Config
from config import settings
from models import Job

logger = logging.getLogger()
logger.setLevel(logging.WARN)

# Used to restrict the number of files downloaded from a study to only those being processed
ALLOWED_EXTENSIONS = ['.vhdr', '.vmrk', '.eeg', '.bdf', '.edf', '.set', '.fdt']

def prepare_study_data(job: Job) -> str:
    """
    Used to download data for the job.
    
    Parameters
    ----------
    job: Job
        Contains details of the job (study processing request).

    Returns
    -------
    The directory the files were downloaded to.
    """
    job_dir = get_download_location(job)
    os.makedirs(job_dir, exist_ok=True)

    s3_client = boto3.client(settings.S3_RESOURCE_NAME, config=Config(signature_version=UNSIGNED))
    response = s3_client.list_objects_v2(Bucket=job.source_db, Prefix=f'{job.study_id}/{job.subject_id}')
    if ('Contents' in response):
        for file in response['Contents']:
            file_name = file['Key']
            if os.path.splitext(file_name)[1] in ALLOWED_EXTENSIONS:
                full_name = f'{job_dir}/{os.path.basename(file_name)}'
                s3_client.download_file(job.source_db, 
                                        file_name, 
                                        full_name)
    return job_dir, get_output_location(job)


def cleanup_files(input_dir: str) -> None:
    """
    Deletes the directory used to temporarily store raw data files while processing.
    
    Parameters:
    ----------
    input_dir: str: 
        The directory containing the raw data files.
    """
    try:
        shutil.rmtree(input_dir)
    except OSError as err:
        logger.error("Could not delete the temporary directory %s: %s: %s", 
                     input_dir,
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])


def get_download_location(job: Job) -> str:
    """
    Returns the location where files for the Job will be downloaded.

    Parameters
    ----------
    job: Job
        The Job to be processed.
    """
    return f'{settings.DOWNLOAD_DIRECTORY}/job-{job.id}-{job.subject_id}'


def get_output_location(job: Job) -> str:
    """
    Returns the location where results for the Job will be saved. 

    Parameters
    ----------
    job: Job
        The Job to be processed.
    """
    return f'{settings.OUTPUT_DIRECTORY}/job-{job.task_id}-{job.subject_id}'