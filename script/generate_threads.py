import logging.config
from config.logging import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

from trends.google_trends import fetch_latest_trends
from search.google_search import GoogleSearch
from scraper.scraper import Scraper
from chatgpt.thread_generator import ThreadGenerator


def main():
    try:
        logger.info("=== Starting process ===")

        # 1. Get the latest trends
        trends = fetch_latest_trends()
        logger.info(f"Found trends: {trends}")

        # 2. Loop through trends to find relevant articles
        for trend in trends:
            googleSearch = GoogleSearch(trend)
            articles = googleSearch.find_best_articles()

            scraper = Scraper(trend)
            for article in articles:
                success = process_article(scraper, trend, article)
                if success:
                    break  # Break out of the loop on success

        logger.info(f"Finished process")

    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise e


def process_article(scraper, trend, article):
    try:
        # 3. Scrape article content
        article_content = scraper.scrape_article(article)

        # 4. Create Twitter threads
        thread_generator = ThreadGenerator(trend)
        thread_generator.generate_thread(article_content)

        return True
    except Exception as e:
        logger.error(f"Failed to process article {article} for trend {trend}: {str(e)}")
        return False


if __name__ == "__main__":
    main()
