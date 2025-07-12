"""
Author: Bathsheba Jackson
Date Created: 2025-07-11
"""
from models.base import Base
from datetime import datetime, timezone
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .job import Job

class File(Base):
    """
    Represents files generated during the processing of a job.
    """
    __tablename__ = "file"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    job_id: Mapped[id] = mapped_column(Integer, ForeignKey("job.id"))
    job: Mapped["Job"] = relationship("Job", back_populates="files")
    subject_id: Mapped[str] = mapped_column(String)
    created_at: Mapped[float] = mapped_column(Float, default=lambda: datetime.now(timezone.utc).timestamp())
    path: Mapped[str] = mapped_column(String, nullable=False)