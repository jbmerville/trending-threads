from aws_cdk import (
    Duration,
    SecretValue,
    Stack,
    aws_sqs as sqs,
    aws_lambda as _lambda,
    aws_lambda_event_sources as lambda_event_sources,
    aws_lambda_python_alpha,
    aws_secretsmanager as secretsmanager,
)
from constructs import Construct
import json

from config import settings


class ThreadStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create DLQ
        dlq = sqs.Queue(
            self,
            f"{id}-DLQ",
            queue_name=f"{id}-DLQ",
            retention_period=Duration.days(14),
        )

        # Create the main SQS queue
        queue = sqs.Queue(
            self,
            f"{id}-Queue",
            queue_name=f"{id}-Queue",
            dead_letter_queue={
                "queue": dlq,
                "max_receive_count": 3,
            },
        )

        twitter_layer = aws_lambda_python_alpha.PythonLayerVersion(
            self,
            f"{id}-TwitterLayer",
            entry=f"lambda/twitter_layer",
            compatible_runtimes=[_lambda.Runtime.PYTHON_3_9],
        )

        # Create Lambda function
        self.lambda_function = _lambda.Function(
            self,
            f"{id}-Lambda",
            function_name=f"{id}-Lambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler=f"handler.handler",  # Path to handler function
            code=_lambda.Code.from_asset("lambda"),  # Path to Lambda code
            layers=[twitter_layer],
            dead_letter_queue=dlq,
            timeout=Duration.seconds(15),
        )

        # Add SQS event source to Lambda
        self.lambda_function.add_event_source(
            lambda_event_sources.SqsEventSource(queue)
        )

        main_account_secret = self.generate_twitter_secret_manager(
            "trends_account",
            settings.TRENDS_TWITTER_API_KEY,
            settings.TRENDS_TWITTER_API_SECRET,
            settings.TRENDS_TWITTER_ACCESS_TOKEN,
            settings.TRENDS_TWITTER_ACCESS_TOKEN_SECRET,
        )

    def generate_twitter_secret_manager(
        self, account_name, api_key, api_secret, access_token, access_token_secret
    ):
        human_readable_account_name = account_name.replace("_", " ")
        logical_id_account_name = "".join(
            [word.capitalize() for word in account_name.split("_")]
        )

        secret = secretsmanager.Secret(
            self,
            f"{logical_id_account_name}Secret",
            description=f"Twitter API Credentials for {human_readable_account_name} account",
            secret_name=f"twitter/credentials/{account_name}",
            secret_object_value={
                "api_key": SecretValue.unsafe_plain_text(api_key),
                "api_secret": SecretValue.unsafe_plain_text(api_secret),
                "access_token": SecretValue.unsafe_plain_text(access_token),
                "access_token_secret": SecretValue.unsafe_plain_text(
                    access_token_secret
                ),
            },
        )
        secret.grant_read(self.lambda_function)
