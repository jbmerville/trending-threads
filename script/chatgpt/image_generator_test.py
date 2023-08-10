import unittest
from unittest.mock import patch
import openai
from chatgpt.image_generator import ImageGenerator


class TestImageGenerator(unittest.TestCase):
    def setUp(self):
        self.trend = "Futuristic Cityscapes"
        self.image_generator = ImageGenerator(self.trend)

    @patch.object(openai.Image, "create")
    def test_generate_image_success(self, mock_create):
        mock_create.return_value = {"data": [{"url": "https://image_url.com"}]}

        result = self.image_generator.generate_image()

        self.assertEqual(result, "https://image_url.com")

    @patch.object(openai.Image, "create")
    def test_generate_image_failure(self, mock_create):
        mock_create.side_effect = Exception("API error")

        with self.assertRaises(Exception) as context:
            self.image_generator.generate_image()

        self.assertTrue(
            "Failed to generate thread from content" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
