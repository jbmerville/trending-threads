import openai
from config.logging import get_trend_logger
from config import settings

openai.api_key = settings.OPENAI_API_KEY


class ImageGenerator:
    def __init__(self, trend):
        self.logger = get_trend_logger(trend)
        self.trend = trend

    def generate_image(self):
        try:
            self.logger.info(f"Genarating image for trend: {self.trend}")

            prompt = f"Generate a twitter thumbnail for the topic: {self.trend}"
            response = openai.Image.create(
                n=1,  # Number of image to generate
                prompt=prompt,
                size="512x512",
                response_format="url",
            )

            self.logger.info(f"ChatGPT response: {response}")

            chat_gpt_image_url = response["data"][0]["url"]

            self.logger.info(f"Image URL: {chat_gpt_image_url}")

            return chat_gpt_image_url

        except Exception as e:
            raise Exception(f"Failed to generate thread from content", e)
