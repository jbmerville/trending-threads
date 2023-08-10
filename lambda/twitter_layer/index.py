import tweepy
import os
import json
import requests
import boto3
from io import BytesIO

from logger import get_thread_logger


class TwitterAPI:
    def __init__(self, thread_name, account_name):
        try:
            self.thread_name = thread_name
            self.logger = get_thread_logger(thread_name)

            # Retrieve the secret from Secrets Manager
            client = boto3.client("secretsmanager")
            response = client.get_secret_value(
                SecretId=f"twitter/credentials/{account_name}"
            )
            credentials = json.loads(response["SecretString"])

            api_key = credentials["api_key"]
            api_secret = credentials["api_secret"]
            access_token = credentials["access_token"]
            access_token_secret = credentials["access_token_secret"]

            # Twitter V1.1 API
            auth = tweepy.OAuth1UserHandler(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )
            self.api = tweepy.API(auth)
            self.api.verify_credentials()

            # Twitter V2 API
            self.client = tweepy.Client(
                consumer_key=api_key,
                consumer_secret=api_secret,
                access_token=access_token,
                access_token_secret=access_token_secret,
            )

            self.logger.info(f"Successfully authenticated with Twitter")
        except Exception as e:
            raise Exception("Failed to authenticate with Twitter", e)

    def post_thread(self, thread, image_url):
        try:
            media_id = self.upload_image(image_url)

            first_tweet = thread[0]
            remaining_tweets = thread[1:]

            previous_tweet_id = self.post_tweet(first_tweet, None, media_id)

            for tweet in remaining_tweets:
                previous_tweet_id = self.post_tweet(tweet, previous_tweet_id)
        except Exception as e:
            raise Exception("Failed to post thread to Twitter", e)

    def post_tweet(self, tweet, previous_tweet_id=None, media_id=None):
        try:
            response = self.client.create_tweet(
                text=tweet,
                in_reply_to_tweet_id=previous_tweet_id,
                media_ids=[media_id] if media_id else None,
            )
            self.logger.info(f"Posted tweet: {response}")
            return response.data["id"]
        except Exception as e:
            raise Exception("Failed to post tweet to Twitter", e)

    def find_thread_file(self, thread_name, directory="threads"):
        # Recursively search for the file in the directory and subdirectories
        for root, _, files in os.walk(directory):
            if thread_name in files:
                return os.path.join(root, thread_name)
        return None

    def post_thread_from_file(self, thread_name, image_url):
        thread_file_path = self.find_thread_file(f"{thread_name}.json")
        self.logger.info(f"Found {thread_name}.json at path: {thread_file_path}")

        if thread_file_path is None:
            raise Exception(f"Thread file '{thread_name}' not found.")

        with open(thread_file_path, "r") as file:
            thread_content = json.load(file)

        self.logger.info(f"Read {thread_name}.json content: {thread_content}")

        media_id = self.upload_image(image_url)

        self.post_thread(thread_content, media_id)

    def upload_image(self, image_url):
        try:
            image_file = self.download_img(image_url)

            # Upload the image
            media = self.api.media_upload(filename="temp.jpg", file=image_file)
            media_id = media.media_id
            return media_id
        except Exception as e:
            raise Exception(f"Failed to upload image from url: {image_url}", e)

    def download_img(self, image_url):
        try:
            # Download the image from the URL
            response = requests.get(image_url)

            self.logger.info(f"Successfully downloaded image from url: {image_url}")
            return BytesIO(response.content)
        except Exception as e:
            raise Exception(f"Failed to download image from url: {image_url}", e)
