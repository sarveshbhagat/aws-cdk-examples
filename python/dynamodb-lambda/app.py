#!/usr/bin/env python3

from aws_cdk import core

from dynamodb_lambda.producer import DynamodbLambdaStack
from dynamodb_lambda.consumer import ConsumerStack

app = core.App()
producer = DynamodbLambdaStack(app, "producer")
consumer = ConsumerStack(app, "consumer", table=producer.get_table())

consumer.add_dependency(producer)

# env={'region': 'us-west-2'}

app.synth()
