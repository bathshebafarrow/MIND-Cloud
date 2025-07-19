"""
Author: Bathsheba Jackson
Date Created: 2025-07-11
"""
from pydantic import BaseModel, ConfigDict

class FileInput(BaseModel):
    job_id: int
    subject_id: str
    path: str
    
    model_config = ConfigDict(extra='ignore') 

class FileResponse(FileInput):
    id: int
    created_at: float