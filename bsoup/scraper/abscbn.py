import requests
from bs4 import BeautifulSoup
import unicodedata

def scrape(URL):
    try:
        output = {}
        print('Getting story for {}'.format(URL))

        page = requests.get(URL, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')

        content = soup.find('div', {'class':'article-content', 'itemprop':'articleBody'})
        tags = soup.find('div', {'class':'article-metakey'})
        output['tags'] = [encode(tag.getText()) for tag in tags.findAll('a')]

        if content is None:
            content = soup.find('div', {'class':'slider-for'})

        if content is None:
            content = soup.find('div', {'class':'media-block'})

        output['videos'] = [tag['src'] for tag in content.findAll('iframe')]
        output['images'] = [tag['src'] for tag in content.findAll('img')]
        output['media'] = [tag['data-instgrm-permalink'] for tag in content.findAll('blockquote', {'class':'instagram-media'})]

        output['text'] = encode(content.getText())
        output['url'] = URL

    except Exception as e:
        print(e)
        output['videos'] = []
        output['images'] = []
        output['text'] = ""
        output['media'] = []
        output['tags'] = []
    return output

# Helper function to remove unnecessary unicode strings
def encode(text):
    return unicodedata.normalize("NFKD", text).strip()

