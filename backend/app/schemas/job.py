"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from pydantic import BaseModel, ConfigDict, Json
from typing import Any, Dict, Optional

class JobInput(BaseModel):
    username: str
    source_db: str
    study_id: str    
    subjects: list[str] = []  
    parameters: dict[str, Any] = {}
    status: str = "CREATED"

    model_config = ConfigDict(extra='ignore') 

class JobResponse(JobInput):
    id: int
    created_at: float
    total_processed: int

class JobUpdate(BaseModel):
    id: int
    status: str

    model_config = ConfigDict(extra='ignore')
