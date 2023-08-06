
import logging

logger = logging.getLogger(__name__)

def generate_thread(content):
    try:
        # your scraping code here
        logger.info(f'Successfully generated thread from content: "{content}"')
    except Exception as e:
        logger.error(f'Failed to generate thread from content: "{content}", error: {str(e)}')