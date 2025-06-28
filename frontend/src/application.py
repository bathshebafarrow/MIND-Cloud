import boto3
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
    application.run(port=8000, debug=True)

def get_db_client():
    session = boto3.Session(aws_access_key_id=application.config['AWS_ACCESS_KEY'],
                            aws_secret_access_key=application.config['AWS_SECRET_KEY'])
    return session.resource('dynamodb', region_name=application.config['AWS_REGION_NAME'])

def get_s3_client():
    return client(
        's3', 
        application.config['AWS_REGION_NAME'],
        aws_access_key_id=application.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=application.config['AWS_SECRET_KEY']
    )

def get_s3_unsigned():
    return client('s3', config=Config(signature_version=UNSIGNED))

def get_internal_bucket():
    return application.config['INTERNAL_BUCKET']

def get_external_bucket():
    return application.config['EXTERNAL_BUCKET']