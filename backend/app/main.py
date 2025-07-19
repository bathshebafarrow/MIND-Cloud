"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from database import engine, SessionLocal
from fastapi import FastAPI
from routes import router
from models import Base
from util.prefill import prefill_data
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:5000"
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(router)

# Create tables
Base.metadata.create_all(bind=engine)

with SessionLocal() as session:
    prefill_data(session)
