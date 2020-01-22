from aws_cdk import (
    core,
    aws_lambda,
    aws_dynamodb,
    aws_events,
    aws_events_targets,
)



class ConsumerStack(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create consumer lambda function
        consumer_lambda = aws_lambda.Function(self, "consumer_lambda_function",
                                              runtime=aws_lambda.Runtime.PYTHON_3_6,
                                              handler="lambda_function.lambda_handler",
                                              code=aws_lambda.Code.asset("./lambda/consumer"))
