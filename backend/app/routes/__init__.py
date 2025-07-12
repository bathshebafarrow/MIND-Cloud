"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from fastapi import APIRouter
from .file import router as file_router
from .jobs import router as job_router

router = APIRouter()
router.include_router(file_router)
router.include_router(job_router)