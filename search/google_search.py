# search/google_search.py

from googleapiclient.discovery import build
import datetime
import logging
from config import settings

logger = logging.getLogger(__name__)


API_KEY = settings.GOOGLE_API_KEY
CSE_ID = settings.GOOGLE_CSE_ID


# List of credible sources (you can modify this list based on your requirements)
CREDIBLE_SOURCES = ['bbc.com', 'nytimes.com', 'cnn.com', 'reuters.com']

def search_articles(trend):
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=trend, cx=CSE_ID).execute()

    best_article = None
    best_score = -1

    for item in res['items']:
        url = item['link']
        snippet = item.get('snippet', '')

        # Check the recency (assuming the search result provides a publication date)
        published_date = datetime.datetime.strptime(item['pagemap']['metatags'][0]['og:updated_time'], '%Y-%m-%d')
        recency_score = (datetime.datetime.now() - published_date).days

        # Check the credibility
        credibility_score = 1 if any(source in url for source in CREDIBLE_SOURCES) else 0

        # Combine the scores to find the best article (you can tweak this logic as needed)
        score = -recency_score + credibility_score * 100

        if score > best_score:
            best_score = score
            best_article = {'url': url, 'snippet': snippet}

    logger.info(f"Found best article for trend '{trend}': {best_article['url']}")
    return best_article
