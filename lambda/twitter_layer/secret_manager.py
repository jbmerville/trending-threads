import boto3
import json


class SecretManager:
    def __init__(self):
        self.client = boto3.client("secretsmanager")

    def get_secret_twitter_credentials(self, account_name):
        try:
            response = self.client.get_secret_value(
                SecretId=f"twitter/credentials/{account_name}"
            )
            credentials = json.loads(response["SecretString"])
            return credentials
        except Exception as e:
            raise Exception(
                f"An error occurred while getting Twitter crenditials for account: {account_name}",
                e,
            )
