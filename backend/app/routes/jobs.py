"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from crud.crud_jobs import create_job, delete_job, retrieve_jobs
from database import get_db
from fastapi import APIRouter, Depends
from schemas.job import JobInput, JobResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/job", tags=["job"])

@router.get("", response_model=JobResponse)
def get_jobs(db: Session = Depends(get_db)):
    return retrieve_jobs(db)
    
@router.post("", response_model=JobResponse)
def post_job(job: JobInput, db: Session = Depends(get_db)):
    return create_job(db, job)

@router.delete("{job_id}")
def remove_job(job_id: int, db: Session = Depends(get_db)):
    delete_job(job_id)
