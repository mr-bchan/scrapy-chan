import requests
from bs4 import BeautifulSoup
import unicodedata

"""
Input: URL
"""
def scrape(URL):
    print('Getting story for {}'.format(URL))
    page = requests.get(URL, verify=False)
    output = parse_body(page.content, URL)
    return output


def parse_body(content, URL):
    soup = BeautifulSoup(content, 'html.parser')
    print('URL: {}'.format(URL))
    output = {}

    tags = soup.find('div', {'class':'article-metakey'})
    timestamp = soup.find('span', {'class':'date-posted'})
    title = soup.find('h1', {'class': 'news-title'})

    content = soup.find('div', {'class':'article-content', 'itemprop':'articleBody'})

    if content is None:
        content = soup.find('div', {'class':'slider-for'})

    if content is None:
        content = soup.find('div', {'class':'media-block'})

    if content is None:
        return output

    output['title'] = title.getText()
    output['videos'] = [tag['src'] for tag in content.findAll('iframe')]
    output['images'] = [tag['src'] for tag in content.findAll('img')]
    output['tags'] = [encode(tag.getText()) for tag in tags.findAll('a')]
    output['text'] = encode(content.getText())
    output['url'] = URL
    output['timestamp'] = timestamp.getText()

    return output

# Helper function to remove unnecessary unicode strings
def encode(text):
    return unicodedata.normalize("NFKD", text).strip()

