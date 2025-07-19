"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from crud.crud_jobs import *
from database import get_db
from fastapi import APIRouter, Depends
from schemas.job import JobInput, JobResponse
from sqlalchemy.orm import Session
from service.producer import get_job_producer, JobProducer

router = APIRouter(prefix="/job", tags=["job"])

@router.get("", response_model=list[JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    return retrieve_jobs(db)

@router.get("/{job_id}", response_model=JobResponse)
def get_jobs(job_id: int, db: Session = Depends(get_db)):
    return retrieve_job(db, job_id)
    
@router.post("", response_model=JobResponse)
def post_job(job: JobInput, db: Session = Depends(get_db), producer: JobProducer = Depends(get_job_producer)):
    return create_job(db, job, producer)

@router.delete("{job_id}")
def remove_job(job_id: int, db: Session = Depends(get_db)):
    delete_job(db, job_id)
