import article_scraper
import json

ENTERTAINMENT_URL = 'https://news.abs-cbn.com/entertainment'
NEWS_URL = 'https://news.abs-cbn.com/news'

URL = ENTERTAINMENT_URL
articles = article_scraper.read_article_list(URL)


# URL = 'https://news.abs-cbn.com/entertainment/04/29/18/i-can-see-your-voice-kim-chiu-fails-in-picking-mr-right'
# article_scraper.read_article('https://news.abs-cbn.com/entertainment/multimedia/slideshow/04/30/18/in-photos-pilipinas-got-talent-grand-finals-night')
