from typing import Any

class JobModel:
    id: int
    username: str
    created_at: float
    source_db: str
    study_id: str    
    subjects: list[str] = []  
    parameters: dict[str, Any]
    total_processed: int
    status: str

    
    