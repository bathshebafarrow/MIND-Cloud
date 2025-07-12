from boto3 import client
from flask import Flask
from botocore import UNSIGNED
from botocore.config import Config

# Create flask application
application = Flask(__name__)

# Load configuration data
application.config.from_pyfile('config.py')

from routes import *

if __name__ == '__main__':
    application.run(port=5000, debug=True)

def get_s3_unsigned():
    return client('s3', config=Config(signature_version=UNSIGNED))

def get_external_bucket():
    return application.config['STUDY_REPO']