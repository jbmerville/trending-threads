import time
import tweepy
import requests
from io import BytesIO
from secret_manager import SecretManager

from logger import get_thread_logger


class TwitterAPI:
    def __init__(self, thread_name, account_name):
        try:
            self.thread_name = thread_name
            self.logger = get_thread_logger(thread_name)

            # Retrieve the secret from Secrets Manager
            secret_manager = SecretManager()
            credentials = secret_manager.get_secret_twitter_credentials(account_name)

            self.authenficate_to_twitter(credentials)
            self.logger.info(f"Successfully initialized the Twitter client")
        except Exception as e:
            raise Exception("An error occured while initializing the Twitter client", e)

    def authenficate_to_twitter(self, credentials):
        try:
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
        except Exception as e:
            raise Exception("Failed to authenticate to Twitter", e)

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
            tweet_id = response.data["id"]
            self.logger.info(f"Successfully posted tweet with tweetId: {tweet_id}")
            return tweet_id
        except Exception as e:
            raise Exception("Failed to post tweet to Twitter", e)

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
