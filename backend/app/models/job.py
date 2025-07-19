"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from datetime import datetime, timezone
from models.base import Base
from models.file import File
from sqlalchemy import ARRAY, Float, Integer, JSON, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any, TYPE_CHECKING


class Job(Base):
    """
    Represents jobs that need to be processed through the application.
    """
    __tablename__ = "job"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[float] = mapped_column(Float, default=lambda: datetime.now(timezone.utc).timestamp())
    modified_at: Mapped[float] = mapped_column(Float, nullable=True)
    source_db: Mapped[str] = mapped_column(String, nullable=False)
    study_id: Mapped[str] = mapped_column(String, nullable=False)    
    subjects: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)   
    total_processed: Mapped[int] = mapped_column(Integer, default=0)
    parameters: Mapped[dict] = mapped_column(JSON, nullable=True) 
    status: Mapped[str] = mapped_column(String, nullable=False)
    files: Mapped[list["File"]] = relationship("File", back_populates="job", lazy="select")
