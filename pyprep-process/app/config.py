# Update to use pydantic

from pydantic import BaseModel

class Settings(BaseModel):
    # Download folder
    DOWNLOAD_FOLDER = '/tmp'

    # The OpenNeuro S3 bucket containing raw EEG and MEG data files. 
    S3_OPENNEURO_URL = 'openneuro.org'

    # The default region when creating new connections.
    S3_REGION_NAME = 'us-east-1'

    JOB_UPDATE_URL = 'http://localhost:500/api/job'

    DEFAULT_MONTAGE = 'standard_1005'

settings = Settings()