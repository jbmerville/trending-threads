import unittest
from unittest.mock import patch, Mock
from scraper.scraper import Scraper


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.trend = "Barcelona"
        self.scraper = Scraper(self.trend)

    @patch("requests.get")
    def test_scrape_article_success(self, mock_get):
        fake_html = (
            """<html><body><p>This is related to Barcelona</p></body></html>""" * 100
        )
        mock_get.return_value = Mock(content=fake_html, status_code=200)
        mock_get.return_value.raise_for_status = Mock()

        url = "http://example.com/article"
        result = self.scraper.scrape_article(url)

        self.assertIn(self.trend, result)

    @patch("requests.get")
    def test_scrape_article_failure(self, mock_get):
        mock_get.return_value.raise_for_status.side_effect = Exception("Request failed")

        url = "http://example.com/failure"
        with self.assertRaises(Exception):
            self.scraper.scrape_article(url)

    def test_is_related_to_trend(self):
        content_related = "This is related to Barcelona"
        self.assertTrue(self.scraper.is_related_to_trend(content_related))

        content_unrelated = "This is not related to the given trend"
        self.assertFalse(self.scraper.is_related_to_trend(content_unrelated))


if __name__ == "__main__":
    unittest.main()
