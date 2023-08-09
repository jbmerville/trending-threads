import tweepy
import os
import json
import requests
from config import settings
from io import BytesIO
from config.logging import get_trend_logger


class TwitterAPI:
    def __init__(self, trend):
        try:
            self.trend = trend
            self.logger = get_trend_logger(trend)

            # Twitter V1.1 API
            auth = tweepy.OAuth1UserHandler(
                consumer_key=settings.TWITTER_API_KEY,
                consumer_secret=settings.TWITTER_API_SECRET,
                access_token=settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            )
            self.api = tweepy.API(auth)
            self.api.verify_credentials()

            # Twitter V2 API
            self.client = tweepy.Client(
                consumer_key=settings.TWITTER_API_KEY,
                consumer_secret=settings.TWITTER_API_SECRET,
                access_token=settings.TWITTER_ACCESS_TOKEN,
                access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET,
            )

            self.logger.info("Successfully authenticated with Twitter")
        except Exception as e:
            raise Exception("Failed to authenticate with Twitter", e)

    def post_thread(self, thread, media_id=None):
        try:
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

        image_file = self.download_img(image_url)

        # Upload the image
        media = self.api.media_upload(filename="temp.jpg", file=image_file)
        media_id = media.media_id

        self.post_thread(thread_content, media_id)

    def download_img(self, image_url):
        try:
            # Download the image from the URL
            response = requests.get(image_url)

            self.logger.info(f"Successfully downloaded image from url: {image_url}")
            return BytesIO(response.content)
        except Exception as e:
            raise Exception(f"Failed to download image from url: {image_url}", e)
