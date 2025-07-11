from crud import create_file_task, retrieve_file_tasks
from database import get_db
from fastapi import APIRouter, Depends
from schemas import FileTaskInput, FileTaskResponse
from sqlalchemy.orm import Session

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=FileTaskResponse)
def get_file_tasks(db: Session = Depends(get_db)):
    return retrieve_file_tasks(db)
    
@router.post("/", response_model=FileTaskResponse)
def create_file_task(task: FileTaskInput, db: Session = Depends(get_db)):
    return create_file_task(db, task)