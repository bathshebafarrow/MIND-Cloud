# Update to use pydantic

# Download folder
DOWNLOAD_FOLDER = 'tmp'

# The secret key for the app.
SECRET_KEY = ''

# The OpenNeuro S3 bucket containing raw EEG and MEG data files. 
S3_OPENNEURO_URL = 'openneuro.org'

# The S3 bucket containing raw files split into 
S3_RAW_FILES = 'eeg-data-raw'

# The S3 bucket containing preprocessed files
S3_PREPROCESSED_FILES = 'eeg-data-clean'

# AWS access key associated with an IAM role or user.
S3_ACCESS_KEY = ''

# A secret key associated with the access key (password).
S3_SECRET_KEY = ''

# The default region when creating new connections.
S3_REGION_NAME = 'us-east-1'

SQS_URL = 'https://sqs.us-east-1.amazonaws.com/XXXXX'