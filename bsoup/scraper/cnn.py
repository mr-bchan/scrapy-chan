import requests
from bs4 import BeautifulSoup
import unicodedata

def scrape(URL):
    try:
        output = {}
        print('Getting story for {}'.format(URL))

        page = requests.get(URL, verify=False)
        soup = BeautifulSoup(page.content, 'html.parser')

        content = soup.find('div', {'class':'article-maincontent-p'}).find('div')

        tags = soup.find('article', {'class':'article-tags'})
        output['tags'] = [encode(tag.getText()) for tag in tags.findAll('a')]

        output['videos'] = []
        output['images'] = [tag['data-proxy-image'].replace('FREE_160', 'FREE_720') for tag in soup.findAll('img',{'class' : 'media-object'})]
        output['text'] = content.getText()
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

