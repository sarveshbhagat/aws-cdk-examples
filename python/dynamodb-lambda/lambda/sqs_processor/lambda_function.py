from __future__ import print_function

import json
import decimal
import os
import boto3
import uuid
import logging
from botocore.exceptions import ClientError

# Set logging
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)

logger = logging.getLogger()
logformat = "[%(asctime)s]%(levelname)s:%(name)s:%(message)s"
logging.basicConfig(stream=sys.stdout, format=logformat,
                    datefmt="%Y-%m-%d %H:%M:%S")
logger.setLevel(logging.INFO)

# Get the service resource.
client_sqs = boto3.client('sqs')

# Environment variable
MESSAGE_BUCKET_NAME = os.environ['MESSAGE_BUCKET_NAME']


def write_message_to_s3(message):
    filename = str(uuid.uuid4())
    json_string = json.dumps(message)
    s3_resource = boto3.resource('s3')
    key = filename + ".json"

    try:
        s3_resource.Object(MESSAGE_BUCKET_NAME, key).put(Body=json_string)

        return True

    except Exception as e:
        # AllAccessDisabled error == bucket not found
        # NoSuchKey or InvalidRequest error == (dest bucket/obj == src bucket/obj)
        logging.error(e)
        return False


def lambda_handler(event, context):
    for record in event['Records']:
        payload = record["body"]
        write_message_to_s3(payload)
        logging.info(str(payload))
