from aws_cdk import (
    core,
    aws_lambda,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
    aws_sqs,
    aws_lambda_event_sources,
aws_s3
)


class ConsumerStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, table=aws_dynamodb.Table, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        # Create Consumer Bucket
        self._message_bucket = aws_s3.Bucket(self, 'ws-message-bucket')

        # Create a sqs queue
        consumer_ingest_queue = aws_sqs.Queue(
            self, "consumer-ingest-queue", queue_name="consumer-ingest-queue",
            visibility_timeout=core.Duration.seconds(300),
        )
        # create consumer lambda function
        consumer_lambda = aws_lambda.Function(self, "consumer_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_6,
                                              handler="lambda_function.lambda_handler",
                                              code=aws_lambda.Code.asset("lambda/consumer"))

        consumer_lambda.add_environment("TABLE_NAME", table.table_name)
        consumer_lambda.add_environment("CONSUMER_QUEUE_NAME", consumer_ingest_queue.queue_name)

        # Add permissions to write to this queue
        consumer_ingest_queue.grant_send_messages(consumer_lambda)
        table.grant_read_data(consumer_lambda)

        # create a Cloudwatch Event rule
        one_minute_rule = aws_events.Rule(
            self, "one_minute_rule",
            schedule=aws_events.Schedule.rate(core.Duration.minutes(2)),
        )

        # Add target to Cloudwatch Event
        one_minute_rule.add_target(aws_events_targets.LambdaFunction(consumer_lambda))

        # create a lambda that gets triggered by the sqs.

        sqs_processor_lambda = aws_lambda.Function(self, "sqs-processor-lambda",
                                                   runtime=aws_lambda.Runtime.PYTHON_3_6,
                                                   handler="lambda_function.lambda_handler",
                                                   code=aws_lambda.Code.asset("lambda/sqs_processor"))
        sqs_processor_lambda.add_environment("MESSAGE_BUCKET_NAME", self._message_bucket.bucket_name)

        # Add permission
        self._message_bucket.grant_write(sqs_processor_lambda)

        # Adding Event Source sqs->lambda
        sqs_event_source = aws_lambda_event_sources.SqsEventSource(
            queue=consumer_ingest_queue,
            batch_size=1
        )

        # Binding the EventSource to Lambda
        sqs_event_source.bind(sqs_processor_lambda)

