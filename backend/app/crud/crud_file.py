"""
Author: Bathsheba Jackson
Date Created: 2025-07-11
"""
from fastapi import HTTPException
from schemas.file import FileInput
from models.file import File
from sqlalchemy import delete
from sqlalchemy.orm import Session

def create_file(db: Session, file: FileInput) -> File:
    """
    Creates a new file record based on the file input.

    Parameters
    ----------
    db: Session
        The database session.
    file: FileInput
        The validated file data.

    Returns
    -------
    The new file record. 
    """
    try:
        new_file = File(**file.model_dump())
        db.add(new_file)
        db.commit()
        db.refresh(new_file)
        return new_file
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail="Could not create a new job"
        )

def retrieve_file(db: Session, file_id: int) -> list[File]:
    return db.query(File).where(File.id == file_id).one_or_none()

def retrieve_files(db: Session) -> list[File]:
    return db.query(File).all()

def delete_file(db: Session, file_id: int):
    try:
        stmt = delete(File).where(File.id == file_id)
        db.execute(stmt)
        db.commit()
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail=f"Could not create delete job {file_id}: {ex}"
        )