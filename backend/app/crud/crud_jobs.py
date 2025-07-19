"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from fastapi import HTTPException
from models.job import Job
from schemas.job import JobInput
from service.producer import JobProducer
from sqlalchemy import delete, select
from sqlalchemy.orm import Session
from typing import List

def create_job(db: Session, job: JobInput, producer: JobProducer) -> Job:
    """
    Creates a new job record based on the file input. The new job
    is added to the queue for processing.

    Parameters
    ----------
    db: Session
        The database session.
    job: JobInput
        The validated job data.
    producer: JobProducer
        Produces job messages on a pulsar topic.

    Returns
    -------
    The new job record. 
    """
    try:
        new_job = Job(**job.model_dump())
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        if producer.publish_tasks(new_job):
            new_job.status = "QUEUED"
            db.commit()
            db.refresh(new_job)
        return new_job
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail="Could not create a new job"
        )

def retrieve_jobs(db: Session) -> List[Job]:
    """
    Retrieves all of the jobs in the database.

    Parameters
    ----------
    db: Session
        The database session.

    Returns
    -------
    The list of Job records.
    """
    try:
        results = db.query(Job).all()
        return results
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail=f"Could not retrieve jobs: {ex}"
        )

def retrieve_job(db: Session, job_id: int) -> Job:
    """
    Retrieves the Job record with the specified unique identifier.

    Parameters
    ----------
    db: Session
        The database session.
    job_id: int
        The unique identifier for the job record to retrieve.

    Returns
    -------
    The list of Job records.
    """
    try:
        result = db.query(Job).where(Job.id == job_id).one_or_none()
        return result
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail=f"Could not retrieve jobs: {ex}"
        )

def delete_job(db: Session, job_id: int):
    """
    Deletes a job from the database.

    Parameters
    ----------
    db: Session
        The database session.
    job_id: int
        The unique identifier for the Job record.
    """
    try:
        stmt = delete(Job).where(Job.id == job_id)
        db.execute(stmt)
        db.commit()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail=f"Could not create delete job {job_id}: {ex}"
        )
