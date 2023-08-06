
import logging

logger = logging.getLogger(__name__)

def post_thread():
    try:
        # your scraping code here
        logger.info(f'Successfully posted threads')
    except Exception as e:
        logger.error(f'Failed to posted threads, error: {str(e)}')