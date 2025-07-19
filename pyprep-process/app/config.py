# Update to use pydantic

from pydantic import BaseModel

class Settings(BaseModel):
    # Folder data files are downloaded to for processing
    DOWNLOAD_FOLDER = '/tmp'
    # The OpenNeuro S3 bucket containing raw EEG and MEG data files. 
    S3_OPENNEURO_URL = 'openneuro.org'

    # API for Job updates
    JOB_UPDATE_URL = 'http://localhost:500/api/job'
    # Pulsar URL for connnections
    PULSAR_URL: str = 'pulsar://pulsar:6650'
    # Pulsar topic that preprocessing jobs are published to
    PREPROCESS_TOPIC: str = 'persistent://public/default/preprocess'

    # Default EEG montage if not selctee
    DEFAULT_MONTAGE = 'standard_1005'

settings = Settings()