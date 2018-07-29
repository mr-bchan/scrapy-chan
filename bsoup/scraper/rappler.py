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

    tags = soup.find('div', {'class':'rappler3-metakey'})
    timestamp = soup.find('div', {'class':'published'})
    title = soup.find('h1', {'class': 'select-headline'})

    content = soup.find('div', {'class':'story-area cXenseParse'})
    if content is not None:
        text = ' '.join([t.getText() for t in content.findAll('p')])
    else:
        return output

    output['title'] = title.getText()
    output['videos'] = [tag['src'] for tag in content.findAll('iframe')]
    output['images'] = [tag['data-original'] for tag in content.findAll('img')]
    output['tags'] = [encode(tag.getText()) for tag in tags.findAll('a')]
    output['text'] = encode(text)
    output['url'] = encode(URL)
    output['timestamp'] = timestamp.getText().replace('Published ', '').strip()

    return output

# Helper function to remove unnecessary unicode strings
def encode(text):
    return unicodedata.normalize("NFKD", text).strip()

