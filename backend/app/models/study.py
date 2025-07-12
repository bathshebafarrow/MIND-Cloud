"""
Author: Bathsheba Jackson
Date Created: 2025-07-11
"""
from models.base import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Repository(Base):
    __tablename__ = "repository"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    bucket_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    studies: Mapped[list["Study"]] = relationship(back_populates="repository", lazy="selectin")

class Study(Base):
    __tablename__ = "study"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    study_id: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    repository_id: Mapped[id] = mapped_column(Integer, ForeignKey("repository.id"))
    repository: Mapped["Repository"] = relationship("Repository", back_populates="studies")
