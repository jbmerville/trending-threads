# tests/test_trends.py

import unittest
from unittest.mock import patch, MagicMock
from trends.google_trends import fetch_latest_trends

class TestGoogleTrends(unittest.TestCase):

    @patch('trends.google_trends.TrendReq')
    def test_fetch_latest_trends(self, MockTrendReq):
        # Create a fake trending searches response
        fake_trends = ['Trend1', 'Trend2', 'Trend3']
        fake_trending_searches_df = MagicMock()
        fake_trending_searches_df.__getitem__.return_value.tolist.return_value = fake_trends

        # Configure the mock TrendReq object to return the fake response
        mock_trend_req_instance = MockTrendReq.return_value
        mock_trend_req_instance.trending_searches.return_value = fake_trending_searches_df

        # Call the function being tested
        trends = fetch_latest_trends()

        # Verify that the function returned the expected result
        self.assertEqual(trends, fake_trends)

    @patch('trends.google_trends.TrendReq')
    def test_fetch_latest_trends_error(self, MockTrendReq):
        # Configure the mock TrendReq object to raise an exception
        mock_trend_req_instance = MockTrendReq.return_value
        mock_trend_req_instance.trending_searches.side_effect = Exception("Error fetching trends")

        # Call the function being tested
        trends = fetch_latest_trends()

        # Verify that the function handled the exception and returned an empty list
        self.assertEqual(trends, [])

if __name__ == '__main__':
    unittest.main()
