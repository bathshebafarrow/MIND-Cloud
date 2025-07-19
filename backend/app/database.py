"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(settings.DATABASE_URL, echo=True)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    with SessionLocal() as session:
        yield session

