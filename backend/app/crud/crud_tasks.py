"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from fastapi import HTTPException
from schemas.task import FileTaskInput
from models.task import FileTask
from sqlalchemy.orm import Session
from typing import List

def create_file_task(db: Session, task: FileTaskInput) -> FileTask:
    try:
        task = FileTask(**task.model_dump())
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except Exception as ex:
        print(ex)
        raise HTTPException(
            status_code=500,
            detail="Could not create a new file processing task"
        )

def retrieve_file_tasks(db: Session) -> List[FileTask]:
    return db.query(FileTask).all()