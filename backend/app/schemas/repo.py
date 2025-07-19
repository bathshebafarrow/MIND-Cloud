"""
Author: Bathsheba Jackson
Date Created: 2025-07-18
"""
from pydantic import BaseModel

class StudyInputModel(BaseModel):
    study_id: str
    description: str
    repository_id: int

class StudyModel(StudyInputModel):
    id: int

class RepositoryInputModel(BaseModel):
    id: int
    bucket_name: str
    display_name: str
    description: str

class RepositoryModel(BaseModel):
    studies: list[StudyModel] = []
