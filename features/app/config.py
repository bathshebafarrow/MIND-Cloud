"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
Last Modified: 2025-07-10
Version: 1.0
"""
from pydantic import BaseModel

class Settings(BaseModel):
    
    PULSAR_TOPIC: str = 'persistent://public/default/feature_tasks'

    PULSAR_SUBSCRIPTION: str = 'feature-extractor'

    PULSAR_HOST: str = 'localhost'
    
    PULSAR_PORT: str = '6650'

settings = Settings()