import logging

logger = logging.getLogger(__name__)

def search_articles(trends):
    try:
        # your scraping code here
        logger.info(f'Successfully scraped article from {trends}')
    except Exception as e:
        logger.error(f'Failed to scrape article from {trends}: {str(e)}')