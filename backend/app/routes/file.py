"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from crud.crud_file import create_file, retrieve_files
from database import get_db
from fastapi import APIRouter, Depends
from schemas.file import FileResponse, FileInput
from sqlalchemy.orm import Session

router = APIRouter(prefix="/file", tags=["file"])

@router.get("", response_model=list[FileResponse])
def get_files(db: Session = Depends(get_db)):
    return retrieve_files(db)
    
@router.post("/", response_model=FileResponse)
def post_file(file: FileInput, db: Session = Depends(get_db)):
    return create_file(db, file)
