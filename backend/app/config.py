"""
Author: Bathsheba Jackson
Date Created: 2025-07-10
"""
from pydantic import BaseModel

class Settings(BaseModel):
    # Preprocess topic name
    PREPROCESS_TOPIC: str = 'persistent://public/default/preprocess'
    # Pulsar URL
    PULSAR_URL: str = 'pulsar://pulsar:6650'
    # Database host 
    DB_HOST: str = 'eeg-db'
    # Database name
    DB_NAME: str = 'eeg-db'
    # Databse user
    DB_USER: str = 'eeg_user'
    # Database login
    DB_PASSWORD: str = 'password'
    # Database port number
    DB_PORT: str = '5432'

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()