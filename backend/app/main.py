"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from database import engine
from fastapi import FastAPI
from routes import router
from models import Base

app = FastAPI()

# Include routers
app.include_router(router)

# Create tables
Base.metadata.create_all(bind=engine)
