"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from pydantic import BaseModel
from typing import Any, Dict, List

class JobInput(BaseModel):
    username: str
    source_db: str
    study_id: str    
    subjects: List[str] = []  
    parameters: Dict[str, Any]
    status: str = "CREATED"

class JobResponse(JobInput):
    id: int
    created_at: float
    total_processed: int

class JobUpdate(JobInput):
    id: int
    total_processed: int
    status: str

