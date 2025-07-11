"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from .base import Base
from datetime import datetime, timezone
from sqlalchemy import ARRAY, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

class FileTask(Base):
    __tablename__ = "file_task"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[float] = mapped_column(Float, default=lambda: datetime.now(timezone.utc).timestamp())
    modified_at: Mapped[float] = mapped_column(Float, nullable=True)
    source_db: Mapped[str] = mapped_column(String, nullable=False)
    study_id: Mapped[str] = mapped_column(String, nullable=False)    
    subjects: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)   
    total_processed: Mapped[int] = mapped_column(Integer, default=0)
    parameters: Mapped[dict] = mapped_column(JSON)  
    status: Mapped[str] 
