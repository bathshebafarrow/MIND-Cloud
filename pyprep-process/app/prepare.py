"""
Research code - downloads files from OpenNeuro.
Created on: Wed Mar 22, 2023
@author: Bathsheba Farrow
"""
import aws_client as aws
import logging
import os
import shutil
from models import Job

logger = logging.getLogger()
logger.setLevel(logging.WARN)

# Used to restrict the number of files downloaded from a study to only those being processed
ALLOWED_EXTENSIONS = ['.vhdr', '.vmrk', '.eeg', '.bdf', '.edf', '.set', '.fdt']

def download_study_data(job: Job) -> str:
    """
    Used to download data for the job.
    
    Parameters
    ----------
    job (Job): 
        Contains details of the job (study processing request).

    Returns
    -------
    The directory the files were downloaded to.
    """
    job_dir = get_download_location(job)
    os.makedirs(job_dir, exist_ok=True)
    s3_client = aws.get_unsigned_client('s3')
    response = s3_client.list_objects_v2(Bucket=job.source_db, Prefix=f'{job.study_id}/{job.subject_id}')
    if ('Contents' in response):
        for file in response['Contents']:
            file_name = file['Key']
            if os.path.splitext(file_name)[1] in ALLOWED_EXTENSIONS:
                full_name = f'{job_dir}/{os.path.basename(file_name)}'
                s3_client.download_file(job.source_db, 
                                        file_name, 
                                        full_name)
    return job_dir

def archive_results(job: Job) -> str:
    """
    Used to upload processed data for entire study. Compresses the data into a zip file
    before uploading.
    
    Parameters:
    ----------
    job (Job): 
        Contains details of the job (study processing request).
    """
    source_dir = f'{get_download_location(job)}/results/'
    archive_file = get_archive_file_path(job)
    shutil.make_archive(archive_file, 'zip', source_dir)
    delete_download_dir(job)
    return f'{archive_file}.zip'


def delete_download_dir(job: Job) -> None:
    """
    Deletes the directory used to temporarily store data files while processing.
    
    Parameters:
    ----------
    job (Job): 
        Contains details of the job (study processing request).
    """
    job_dir = get_download_location(job)
    try:
        shutil.rmtree(job_dir)
    except OSError as err:
        logger.error("Could not delete the temporary directory %s: %s: %s", 
                     job_dir,
                     err.response['Error']['Code'],
                     err.response['Error']['Message'])


def get_download_location(job: Job) -> str:
    return f'/tmp/job-{job.id}-{job.subject_id}'

def get_archive_file_path(job: Job) -> str:
    return f'/preprocessed/job-{job.task_id}/{job.subject_id}_eeg_processed_data'