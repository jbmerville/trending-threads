from pytrends.request import TrendReq
import logging

logger = logging.getLogger(__name__)

def fetch_latest_trends():

    # Create a pytrends object
    pytrends = TrendReq(hl='en-US', tz=360)

    try:
        logger.info(f"Starting fetching of trending topics from Google Trends.")

        # Get the top trending searches over the past 24 hours in the US
        trending_searches_df = pytrends.trending_searches(pn='united_states')
        trends = trending_searches_df[0].tolist()

        logger.info(f"Fetched {len(trends)} trending topics from Google Trends.")
        return trends

    except Exception as e:
        logger.error(f"Failed to fetch trending topics from Google Trends: {str(e)}")
        return []