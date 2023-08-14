import json
import logging.config
from twitter_layer.dynamodb import DynamoDB
from logger import get_thread_logger
from logger import LOGGING_CONFIG

from twitter_layer.index import TwitterAPI

logging.config.dictConfig(LOGGING_CONFIG)


def handler(event, context):
    try:
        for record in event["Records"]:
            message_body = json.loads(record["body"])
            thread_name = message_body["thread_name"]
            thread_content = message_body["thread_content"]
            account_name = message_body["account_name"]
            image_url = message_body["image_url"]

            logger = get_thread_logger(thread_name)

            logger.info(
                f"Received message with input thread_name: '{thread_name}', account_name: '{account_name}', image_url: '{image_url}', thread_content: '{thread_content}'"
            )

            validate_input(thread_name, thread_content, account_name, image_url)

            # End early if thread already sent
            dynamodb = DynamoDB(thread_name)
            if dynamodb.is_thread_already_processed():
                logger.info(f"Thread already processed, ending execution early")
                return {"statusCode": 200}

            twitter_api = TwitterAPI(thread_name, account_name)
            twitter_api.post_thread(thread_content, image_url)

            dynamodb.mark_thread_as_sent(account_name)
        return {"statusCode": 200}
    except Exception as e:
        logger.error(
            f"An error occurred while processing message: {event['Records']}",
            e,
        )
        return {"statusCode": 500}


def validate_input(thread_name, thread_content, account_name, image_url):
    if thread_name == None or thread_name == "":
        raise Exception(f"Input thread_name is invalid, was: {thread_name}")
    if account_name == None or account_name == "":
        raise Exception(f"Input account_name is invalid, was: {account_name}")
    if image_url == None or image_url == "":
        raise Exception(f"Input image_url is invalid, was: {image_url}")
    if type(thread_content) != list or len(thread_content) == 0:
        raise Exception(f"Input thread_content is invalid, was: {thread_content}")
