"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from pydantic import BaseModel

class Settings(BaseModel):

    PREPROCESS_TOPIC: str = 'persistent://public/default/preprocess'

    PULSAR_URL: str = 'pulsar://pulsar:6650'
    
    DB_HOST: str = 'eeg-db'

    DB_NAME: str = 'eeg-db'
    
    DB_USER: str = 'eeg_user'

    DB_PASSWORD: str = 'password'

    DB_PORT: str = '5432'

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()