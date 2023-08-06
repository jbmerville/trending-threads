import logging.config
from config.logging import LOGGING_CONFIG

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from trends.google_trends import fetch_latest_trends
from search.google_search import search_articles
from scraper.scraper import scrape_article
from chatgpt.thread_generator import generate_thread
from twitter.twitter_api import post_thread

def main():
    try:
        logger.info("Starting process")

        # 1. Get the latest trends
        trends = fetch_latest_trends()
        logger.info("Fetched latest trends")

        # 2. Loop through trends to find relevant articles
        for trend in trends:
            articles = search_articles(trend)
            logger.info(f"Found articles for trend {trend}")

            # 3. Scrape article content and create Twitter threads
            for article in articles:
                content = scrape_article(article['url'])
                twitter_thread = generate_thread(content)
                logger.info(f"Generated Twitter thread for article {article['url']}")

                # 4. Post the Twitter thread
                post_thread(twitter_thread)
                logger.info(f"Posted Twitter thread for trend {trend}")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
