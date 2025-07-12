"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from service.producer import publish_preprocessing_tasks
from fastapi import HTTPException
from schemas.job import JobInput
from models.job import Job 
from sqlalchemy import delete
from sqlalchemy.orm import Session
from typing import List

def create_job(db: Session, job: JobInput) -> Job:
    """
    Creates a new job record based on the file input. The new job
    is added to the queue for processing.

    Parameters
    ----------
    db: Session
        The database session.
    job: JobInput
        The validated job data.

    Returns
    -------
    The new job record. 
    """
    try:
        new_job = Job(**job.model_dump())
        db.add(new_job)
        db.commit()
        db.refresh(new_job)
        if publish_preprocessing_tasks(new_job):
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
    return db.query(Job).all()

def delete_job(db: Session, job_id: int):
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