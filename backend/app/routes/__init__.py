"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from fastapi import APIRouter
from .tasks import router as task_router

router = APIRouter()
router.include_router(task_router)