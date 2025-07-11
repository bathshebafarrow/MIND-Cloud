from pydantic import BaseModel
from typing import Any, Dict


class SubjectTask(BaseModel):
    id: int
    source_db: str
    study_id: str    
    subject_id: id 
    parameters: Dict[str, Any]

class TaskUpdate(BaseModel):
    id: int
    status: str
