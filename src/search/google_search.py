from googleapiclient.discovery import build
import datetime
from config import settings
from dateutil.parser import parse
from dateutil.tz import tzlocal

from config.logging import get_trend_logger

# List of credible sources (you can modify this list based on your requirements)
CREDIBLE_SOURCES = ["bbc.com", "nytimes.com", "cnn.com", "reuters.com"]


class GoogleSearch:
    def __init__(self, trend):
        self.logger = get_trend_logger(trend)
        self.trend = trend
        self.discovery = build(
            "customsearch", "v1", developerKey=settings.GOOGLE_API_KEY
        )

    def find_best_articles(self):
        try:
            self.logger.info(f"Step 1: Google search for articles on the trend")

            res = (
                self.discovery.cse()
                .list(q=f"{self.trend} latest news", cx=settings.GOOGLE_CSE_ID)
                .execute()
            )

            ranked_articles = GoogleSearch.rank_articles(res["items"])

            self.logger.info(
                f"Found {len(ranked_articles)} articles: {ranked_articles}"
            )
            return ranked_articles

        except Exception as e:
            raise Exception("Failed to fetch trending topics from Google trends", e)

    @staticmethod
    def rank_articles(items):
        articles = []

        for item in items:
            url = item["link"]
            snippet = item.get("snippet", "")

            # Check the credibility
            credibility_score = (
                1 if any(source in url for source in CREDIBLE_SOURCES) else 0
            )

            # Check the recency
            recency_score = GoogleSearch.get_recency_score(item)

            # Combine the scores to rank the articles
            score = -recency_score + credibility_score * 100

            articles.append({"url": url, "snippet": snippet, "score": score})

        # Sort the articles by score, from best to worst
        sorted_articles = sorted(articles, key=lambda x: x["score"], reverse=True)

        return [article["url"] for article in sorted_articles]

    @staticmethod
    def get_recency_score(item):
        try:
            metatags = item.get("pagemap", {}).get("metatags", [{}])
            og_updated_time = metatags[0].get("og:updated_time", None)

            if og_updated_time:
                date_str = item["pagemap"]["metatags"][0]["og:updated_time"]
                published_date = (
                    parse(date_str).astimezone(tzlocal()).replace(tzinfo=None)
                )
                current_date = datetime.datetime.now()
                return (current_date - published_date).days
            return 365  # We default to one year if no date is found
        except Exception as e:
            raise Exception(f"Failed get recency score. Item: {item}", e)
