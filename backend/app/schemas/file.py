"""
Author: Bathsheba Jackson
Date Created: 2025-07-11
"""
from pydantic import BaseModel

class FileInput(BaseModel):
    job_id: int
    subject_id: str
    path: str

class FileResponse(FileInput):
    id: int
    created_at: float