import requests
from bs4 import BeautifulSoup
import unicodedata

def read_article_list(URL):

    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    articles = soup.find_all('article', class_='clearfix')

    output_articles = []

    for article in articles:

        formatted_article = {}
        link =  article.find('a')

        # Get URL
        formatted_article['url'] = URL.rsplit('/',1)[0] + link['href']

        # Get images (thumbnail)
        formatted_article['image'] = link.find('img')['src'].split('_')[0] + '.jpg'

        # Get text
        formatted_article['summary'] = encode(article.find('p',{'class': None}).getText().split('\n')[0])
        formatted_article['title'] = encode(article.find('p',{'class' : 'title'}).getText())

        # Get date
        formatted_article['timestamp'] = article.find('span',{'class':'datetime'}).getText()

        story = read_article(formatted_article['url'])
        formatted_article['story'] = story['text']
        formatted_article['image'] = [formatted_article['image']] + story['images']
        formatted_article['video'] = story['videos']
        formatted_article['tags'] = story['tags']
        formatted_article['media'] = story['media']

        print(formatted_article)

        output_articles.append(formatted_article)

    print('Number of articles scraped: ' + str(len(output_articles)))
    return output_articles

def read_article(URL):

    try:
        print('Getting story for {}'.format(URL))

        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        content = soup.find('div', {'class':'article-content', 'itemprop':'articleBody'})
        tags = soup.find('div', {'class':'article-metakey'})

        if content is None:
            content = soup.find('div', {'class':'slider-for'})

        output = {}
        output['videos'] = [tag['src'] for tag in content.findAll('iframe')]
        output['images'] = [tag['src'] for tag in content.findAll('img')]
        output['media'] = [tag['data-instgrm-permalink'] for tag in content.findAll('blockquote', {'class':'instagram-media'})]

        output['text'] = encode(content.getText())
        output['url'] = URL
        output['tags'] = [encode(tag.getText()) for tag in tags.findAll('a')]

    except Exception as e:
        print(e)
        output['url'] = URL
        output = {}
        output['videos'] = []
        output['images'] = []
        output['text'] = ""
        output['tags'] = []
        output['media'] = []


    return output

# Helper function to remove unnecessary unicode strings
def encode(text):
    return unicodedata.normalize("NFKD", text).strip()