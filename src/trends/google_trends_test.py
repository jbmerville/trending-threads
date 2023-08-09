import unittest
from unittest.mock import patch, MagicMock
from trends.google_trends import fetch_latest_trends


class TestGoogleTrends(unittest.TestCase):
    @patch("trends.google_trends.TrendReq")
    def test_fetch_latest_trends(self, MockTrendReq):
        fake_trends = ["Trend1", "Trend2", "Trend3"]
        fake_trending_searches_df = MagicMock()
        fake_trending_searches_df.__getitem__.return_value.tolist.return_value = (
            fake_trends
        )

        mock_trend_req_instance = MockTrendReq.return_value
        mock_trend_req_instance.trending_searches.return_value = (
            fake_trending_searches_df
        )

        trends = fetch_latest_trends()

        self.assertEqual(trends, fake_trends)

    @patch("trends.google_trends.TrendReq")
    def test_fetch_latest_trends_error(self, MockTrendReq):
        mock_trend_req_instance = MockTrendReq.return_value
        mock_trend_req_instance.trending_searches.side_effect = Exception(
            "Error fetching trends"
        )

        trends = fetch_latest_trends()

        self.assertEqual(trends, [])


if __name__ == "__main__":
    unittest.main()
