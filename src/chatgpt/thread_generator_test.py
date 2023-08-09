import unittest
from unittest.mock import patch

import openai
from chatgpt.thread_generator import ThreadGenerator


class TestThreadGenerator(unittest.TestCase):
    def setUp(self):
        self.trend = "Artificial Intelligence"
        self.thread_generator = ThreadGenerator(self.trend)
        self.article_content = "Article content for testing."

    @patch.object(ThreadGenerator, "summarize_article")
    @patch.object(openai.Completion, "create")
    def test_generate_thread_success(self, mock_create, mock_summarize):
        mock_summarize.return_value = "Summarized content"
        mock_create.return_value = {
            "choices": [
                {
                    "text": """
                
Thread 1: 

Climate change is one of the most pressing issues of our time. It's already having an impact on the environment, and the consequences will only get worse if we don't act now.

Thread 2: 

The impacts of climate change are far-reaching and can be seen in extreme weather events, rising sea levels, and changes in ecosystems. It's also having an impact on human health, with an increase in air pollution and disease.

Thread 3: 

We can take action to reduce the effects of climate change. This includes reducing emissions, conserving energy, and investing in renewable energy sources. It's up to us to make sure we protect our planet for future generations. #ClimateChange #ActNow"""
                }
            ]
        }

        result = self.thread_generator.generate_thread(self.article_content)

        self.assertEqual(
            result,
            [
                "Climate change is one of the most pressing issues of our time. It's already having an impact on the environment, and the consequences will only get worse if we don't act now.",
                "The impacts of climate change are far-reaching and can be seen in extreme weather events, rising sea levels, and changes in ecosystems. It's also having an impact on human health, with an increase in air pollution and disease.",
                "We can take action to reduce the effects of climate change. This includes reducing emissions, conserving energy, and investing in renewable energy sources. It's up to us to make sure we protect our planet for future generations. #ClimateChange #ActNow",
            ],
        )

    @patch.object(ThreadGenerator, "extract_threads")
    def test_generate_thread_failure(self, mock_extract):
        mock_extract.side_effect = Exception("No threads found")

        with self.assertRaises(Exception) as context:
            self.thread_generator.generate_thread(self.article_content)

        self.assertTrue(
            "Failed to generate thread from content" in str(context.exception)
        )

    def test_extract_threads_success(self):
        text = """Thread 1: Content 1.
        Thread 2: Content 2."""

        result = ThreadGenerator.extract_threads(text)

        self.assertEqual(result, ["Content 1.", "Content 2."])

    def test_extract_threads_failure(self):
        text = "No threads here."

        with self.assertRaises(Exception) as context:
            ThreadGenerator.extract_threads(text)

        self.assertTrue("No threads found" in str(context.exception))


if __name__ == "__main__":
    unittest.main()
