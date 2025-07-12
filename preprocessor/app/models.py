from pydantic import BaseModel
from typing import Any, Dict


class Job(BaseModel):
    id: int
    source_db: str
    study_id: str    
    subject_id: id 
    parameters: Dict[str, Any]

class JobUpdate(BaseModel):
    id: int
    status: str
