
import logging

logger = logging.getLogger(__name__)

def scrape_article(url):
    try:
        # your scraping code here
        logger.info(f'Successfully scraped article from {url}')
    except Exception as e:
        logger.error(f'Failed to scrape article from {url}: {str(e)}')