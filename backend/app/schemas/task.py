"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from pydantic import BaseModel
from typing import Any, Dict, List

class FileTaskInput(BaseModel):
    username: str
    source_db: str
    study_id: str    
    subjects: List[str] = []  
    parameters: Dict[str, Any]
    status: str = "CREATED"

class FileTaskResponse(FileTaskInput):
    id: int
    created_at: float
    total_processed: int

    class Config:
        orm_mode = True