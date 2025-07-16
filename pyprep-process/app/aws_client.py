import app.config as config
import boto3
from botocore import UNSIGNED
from botocore.config import Config

def get_signed_client(resource_type):
    return boto3.client(resource_type, 
                   region_name=config.S3_REGION_NAME,
                   aws_access_key_id=config.S3_ACCESS_KEY,
                   aws_secret_access_key=config.S3_SECRET_KEY)

def get_unsigned_client(resource_type):
    return boto3.client(resource_type, config=Config(signature_version=UNSIGNED))

def get_db_client():
    session = boto3.Session(aws_access_key_id=config.S3_ACCESS_KEY,
                   aws_secret_access_key=config.S3_SECRET_KEY)
    return session.resource('dynamodb', region_name=config.S3_REGION_NAME)

def get_public_client(resource_type):
    return boto3.client(resource_type, config=Config(signature_version=UNSIGNED))

