from __future__ import print_function

import json
import decimal
import os
import boto3
from botocore.exceptions import ClientError
import uuid


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if o % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


# Get the service resource
sqs = boto3.resource('sqs')
dynamodb = boto3.resource('dynamodb')


# set environment variable
TABLE_NAME = os.environ['TABLE_NAME']
CONSUMER_QUEUE_NAME = os.environ['CONSUMER_QUEUE_NAME']



def lambda_handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    message = []
    # Scan items in table
    try:
        response = table.scan()
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        # print item of the table - see CloudWatch logs
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))
            message.append(json.dumps(i))


    queue = sqs.get_queue_by_name(QueueName=CONSUMER_QUEUE_NAME)
    # Create a new message
    response = queue.send_message(MessageBody=str(message))

    # The response is NOT a resource, but gives you a message ID and MD5
    print(response.get('MessageId'))

    return {
        'statusCode': 200,
    }



