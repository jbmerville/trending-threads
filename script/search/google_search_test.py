import unittest
from unittest.mock import patch, MagicMock
from search.google_search import GoogleSearch


class TestGoogleSearch(unittest.TestCase):
    def setUp(self):
        self.trend = "Technology"
        self.google_search = GoogleSearch(self.trend)

    @patch.object(GoogleSearch, "rank_articles")
    @patch("googleapiclient.discovery.build")
    def test_find_best_articles_success(self, mock_build, mock_rank):
        mock_build.return_value.cse().list().execute.return_value = {"items": []}
        mock_rank.return_value = ["url1", "url2"]

        result = self.google_search.find_best_articles()

        self.assertEqual(result, ["url1", "url2"])

    def test_rank_articles(self):
        items = [
            {
                "link": "http://bbc.com/article1",
                "snippet": "Snippet 1",
                "pagemap": {"metatags": [{"og:updated_time": "2022-08-05T12:00:00"}]},
            },
            {
                "link": "http://example.com/article2",
                "snippet": "Snippet 2",
            },
        ]

        result = GoogleSearch.rank_articles(items)

        self.assertEqual(
            result, ["http://bbc.com/article1", "http://example.com/article2"]
        )

    def test_get_recency_score_with_date(self):
        item = {"pagemap": {"metatags": [{"og:updated_time": "2022-08-05T12:00:00"}]}}

        result = GoogleSearch.get_recency_score(item)

        self.assertTrue(isinstance(result, int))
        self.assertTrue(result >= 0)

    def test_get_recency_score_no_date(self):
        item = {"pagemap": {"metatags": [{}]}}

        result = GoogleSearch.get_recency_score(item)

        self.assertEqual(result, 365)


if __name__ == "__main__":
    unittest.main()
