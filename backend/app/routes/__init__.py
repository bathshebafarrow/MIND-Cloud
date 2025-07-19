"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from fastapi import APIRouter
from routes.file import router as file_router
from routes.jobs import router as job_router
from routes.repo import router as repo_router

router = APIRouter()
router.include_router(file_router)
router.include_router(job_router)
router.include_router(repo_router)