from pydantic import BaseModel
from typing import Any


class Job(BaseModel):
    id: int
    username: str
    source_db: str
    study_id: str    
    subjects: list[str] = []  
    parameters: dict[str, Any] = {}
    created_at: float
    total_processed: int
    status: str

class JobUpdate(BaseModel):
    id: int
    status: str
