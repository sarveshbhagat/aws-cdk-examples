#!/usr/bin/env python3

from aws_cdk import core

from dynamodb_lambda.dynamodb_lambda_stack import DynamodbLambdaStack


app = core.App()
DynamodbLambdaStack(app, "dynamodb-lambda")
#env={'region': 'us-west-2'}

app.synth()
