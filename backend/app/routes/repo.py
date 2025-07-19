"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from crud.crud_repo import *
from database import get_db
from fastapi import APIRouter, Depends
from schemas.repo import StudyModel, RepositoryModel
from sqlalchemy.orm import Session


router = APIRouter(prefix="/repo", tags=["repo"])

@router.get("", response_model=list[RepositoryModel])
def get_repositories(db: Session = Depends(get_db)):
    return retrieve_repositories(db)

@router.get("/study/", response_model=list[StudyModel])
def get_studies(db: Session = Depends(get_db)):
    return retrieve_studies(db)