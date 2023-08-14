import openai
from config import settings
import os
import re
import json
from datetime import datetime
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from config.logging import get_trend_logger


openai.api_key = settings.OPENAI_API_KEY
SUMMARY_SENTENCE_COUNT = 15


class ThreadGenerator:
    def __init__(self, trend):
        self.logger = get_trend_logger(trend)
        self.trend = trend

    def generate_thread(self, article_content):
        try:
            self.logger.info(f"Step 3: Genarating thread from article content")

            summarized_article = self.summarize_article(article_content)
            self.logger.info(
                f"Summarized the article down to {SUMMARY_SENTENCE_COUNT} sentences: {summarized_article}"
            )

            prompt = f"Please summarize the following article content into a series of Twitter threads. Keep in mind that there might be some unrelated content to the topci {self.trend}, so focus on only the relevant points. The outputed thread should be not mention the article but simply explain why this topic is trending and give informative data on the topic. Note that each thread should not go over 280 characters. Please add hashtags at the end of each thread:\n{summarized_article}"
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=280
                * 5,  # Adjust this value to control the length of the summary
                temperature=0.5,
            )

            chat_gpt_threads = response["choices"][0]["text"]

            self.logger.info(f"ChatGPT response: {chat_gpt_threads}")

            threads = ThreadGenerator.extract_threads(chat_gpt_threads)

            self.logger.info(f"Extracted threads: {threads}")

            self.store_thread(threads)

            return threads

        except Exception as e:
            raise Exception(f"Failed to generate thread from content", e)

    def store_thread(self, threads):
        try:
            title = "".join([c if c.isalnum() else "_" for c in self.trend])

            folder_name = os.path.join("threads", datetime.now().strftime("%Y-%m-%d"))

            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            file_path = os.path.join(folder_name, title + ".json")

            with open(file_path, "w", encoding="utf-8") as file:
                thread_input = self.generate_thread_input(threads)
                json.dump(thread_input, file, indent=2)

            self.logger.info(f"Thread stored in {file_path}")
        except Exception as e:
            self.logger.error(f"Failed to store thread", e)

    def summarize_article(self, article_content):
        try:
            parser = PlaintextParser.from_string(article_content, Tokenizer("english"))
            summarizer = LsaSummarizer()
            summary = summarizer(parser.document, SUMMARY_SENTENCE_COUNT)
            summarized_article_content = " ".join(
                [str(sentence) for sentence in summary]
            )

            self.logger.info(f"Summarized article: {summarized_article_content}")

            return summarized_article_content
        except Exception as e:
            raise Exception(f"Failed to summarize article content", e)

    def generate_thread_input(self, threads):
        return {
            "thread_content": threads,
            "thread_name": self.trend,
            "schedule": "",
            "account_name": "trends_account",
            "image_url": "",
        }

    @staticmethod
    def extract_threads(text):
        thread_pattern = r"Thread \d+:\s+(.*)"
        threads = re.findall(thread_pattern, text)

        if len(threads) == 0:
            return [value for value in text.split("\n") if value != ""]

        return threads
