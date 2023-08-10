from bs4 import BeautifulSoup
import requests
import spacy

from config.logging import get_trend_logger


class Scraper:
    def __init__(self, trend):
        self.logger = get_trend_logger(trend)
        self.logger.info(f"Step 2: Scraping articles until one lets us scrape it")
        self.trend = trend

    def scrape_article(self, url):
        try:
            self.logger.info(f"Attempting to scrape artcile at URL: {url}")

            # Send a GET request to the URL
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            # Parse the HTML content of the page
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract and concatenate all the text within <p> tags
            article_content = " ".join(p.get_text() for p in soup.find_all("p"))
            self.logger.info(
                f"Successfully scraped article for content: {article_content}"
            )

            if len(article_content) < 1000:
                raise Exception(f"Article content at URL: {url} was too small")

            if not self.is_related_to_trend(article_content):
                raise Exception(
                    f"Article content at URL: {url} is not related enough to the trend"
                )

            return article_content

        except Exception as e:
            raise Exception(f"Failed to scrape article at URL: {url}", e)

    def is_related_to_trend(self, article_content):
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(article_content)
        for keyword in self.trend.split():
            for token in doc:
                if token.text.lower() == keyword.lower():
                    return True
        return False
