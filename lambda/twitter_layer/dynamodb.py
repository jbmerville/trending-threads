import boto3

from logger import get_thread_logger
from datetime import datetime


class DynamoDB:
    def __init__(self, thread_name):
        self.thread_name = thread_name
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table("TrendingThread-Table")
        self.logger = get_thread_logger(thread_name)

    def is_thread_already_processed(self):
        try:
            response = self.table.get_item(Key={"thread_name": self.thread_name})
            if "Item" in response:
                self.logger.warning(
                    f"Thread {self.thread_name} has already been processed"
                )

                return True
            self.logger.info(f"Thread {self.thread_name} has not been processed before")
            return False
        except Exception as e:
            raise Exception(
                f"An error occurred while checking if thread: {self.thread_name} is already processed",
                e,
            )

    def mark_thread_as_sent(self, account_name):
        try:
            response = self.table.put_item(
                Item={
                    "thread_name": self.thread_name,
                    "status": "processed",
                    "account_name": account_name,
                    "processed_at": datetime.now().isoformat(),
                }
            )
            if "Item" in response:
                self.logger.error(
                    f"Successfully updated dynamodb to mark thread: {self.thread_name} as processed"
                )

                return True
            return False
        except Exception as e:
            raise Exception(
                f"An error occurred while updating dynamodb to mark thread: {self.thread_name} as processed",
                e,
            )
