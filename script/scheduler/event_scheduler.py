from datetime import datetime, timedelta
import json
import logging
import os
import boto3

from config.settings import QUEUE_ARN, ROLE_ARN

logger = logging.getLogger(__name__)


class EventScheduler:
    def __init__(self, minute_interval=30, start_date=None):
        self.events_client = boto3.client("events")
        self.scheduler_client = boto3.client("scheduler")
        self.minute_interval = minute_interval
        self.start_date = start_date

    def schedule_events(self, thread_names):
        for index, thread_name in enumerate(thread_names):
            thread = EventScheduler.read_thread_content(thread_name)
            EventScheduler.validate_thread_content(thread)
            self.call_create_schedule(thread, index)

    def call_create_schedule(self, thread, offset=1):
        try:
            logger.info(f"Starting call to AWS Event Scheduler CreateSchedule")

            target = {
                "Arn": QUEUE_ARN,
                "RoleArn": ROLE_ARN,
                "Input": json.dumps(thread),
            }

            response = self.scheduler_client.create_schedule(
                Name=f"messages-scheduler-{thread['thread_name'].replace(' ', '-')}-{datetime.now().strftime('%Y-%m-%d')}",
                Target=target,
                ActionAfterCompletion="DELETE",
                FlexibleTimeWindow={"Mode": "OFF"},
                ScheduleExpression=self.get_execution_time(offset),
            )

            logger.info(f"AWS Event Scheduler CreateSchedule response was: {response}")
            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise Exception(
                    f"AWS Event Scheduler CreateSchedule failed with resonse: {response}"
                )
        except Exception as e:
            raise Exception(
                f"An error occurred while calling AWS Event Scheduler CreateScheduler",
                e,
            )

    def get_execution_time(self, offset):
        current_date = datetime.utcnow()
        time_delta = timedelta(minutes=self.minute_interval * offset)
        default_5min_delta = timedelta(minutes=5)
        new_date = current_date + time_delta + default_5min_delta

        return f"at({new_date.strftime('%Y-%m-%dT%H:%M:%S')})"

    @staticmethod
    def find_thread_file(thread_name, directory="../threads"):
        file_name = f"{thread_name}.json"

        # Recursively search for the file in the directory and subdirectories
        for root, _, files in os.walk(directory):
            if file_name in files:
                thread_path = os.path.join(root, file_name)
                logger.info(f"Found {file_name} at path: '{thread_path}'")
                return thread_path
        raise Exception(f"Thread file:'{file_name} not found")

    @staticmethod
    def read_thread_content(thread_name):
        try:
            file_path = EventScheduler.find_thread_file(thread_name)
            thread = json.load(open(file_path, "r"))

            logger.info(f"Successfully read thread json: {thread}")
            return thread
        except Exception as e:
            raise Exception(f"An error occurred while reading thread json", e)

    @staticmethod
    def validate_thread_content(thread):
        thread_name = thread["thread_name"]
        thread_content = thread["thread_content"]
        account_name = thread["account_name"]
        image_url = thread["image_url"]

        if thread_name == None or thread_name == "":
            raise Exception(f"Input thread_name is invalid, was: {thread_name}")
        if account_name == None or account_name == "":
            raise Exception(f"Input account_name is invalid, was: {account_name}")
        if image_url == None or image_url == "":
            raise Exception(f"Input image_url is invalid, was: {image_url}")
        if type(thread_content) != list or len(thread_content) == 0:
            raise Exception(f"Input thread_content is invalid, was: {thread_content}")
