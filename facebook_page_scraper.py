# Script to read Facebook Page posts using Facebook Graph API
# Input
# @ FACEBOOK_PAGE_ID
# @ ACCESS TOKEN - valid and not expired

from bsoup import article_scraper as scraper
import requests
import json
import datetime
import time

def read_posts(url, source):
    print('URL: {}'.format(url))
    content = requests.get(url).json()

    if 'posts' in content:
        posts = content['posts']['data']
        next_url = content['posts']['paging']['next']
    else:
        posts = content['data']
        next_url = content['paging']['next']

    data = []

    for post in posts:

        try:
            article = {'id': post['id'],
                       'timestamp': post['created_time'],
                       'summary': post['message'],
                       'link': post['link'],
                       'type': post['status_type'],
                       'likes' : post['like']['summary']['total_count'],
                       'comments' : post['comments']['summary']['total_count']
            }
        except Exception as e:
            continue

        try:
            article['shares'] = post['shares']['count']
        except Exception:
            article['shares'] = 0



        try:

            if 'subattachments' in post['attachments']['data']:
                article['attachments'] = post['attachments']['data']['subattachments']
            else:
                article['attachments'] = post['attachments']['data']

            article['description'] = article['attachments'][0]['description']
            article['title'] = article['attachments'][0]['title']

        except Exception as e:
            article['attachments'] = []
            article['description'] = ""
            article['title'] = ""


        # scraped_data = scraper.read_article(article['link'])
        # article['tags'] = scraped_data['tags']
        # article['videos'] = scraped_data['videos']
        # article['images'] = scraped_data['images']
        # article['full_text'] = scraped_data['text']

        # Add news source
        article['tag'] = ['@' + source]

        data.append(article)

    return {'data':data, 'next':next_url}


def scrape_page(FACEBOOK_PAGE_ID, ACCESS_TOKEN):
    URL = 'https://graph.facebook.com/v2.12/' + FACEBOOK_PAGE_ID +\
          '?fields=posts.limit(100)' \
          '{id,created_time,message,attachments,link,permalink_url,shares,%20status_type,%20comments.limit(0).summary(true),reactions.type(LIKE).summary(total_count).as(like),reactions.type(LOVE).summary(total_count).as(love),reactions.type(HAHA).summary(total_count).as(haha),reactions.type(WOW).summary(total_count).as(wow),reactions.type(SAD).summary(total_count).as(sad),reactions.type(ANGRY).summary(total_count).as(angry)}&access_token=' + ACCESS_TOKEN + '&pretty=0;'

    articles = []

    data = read_posts(URL, FACEBOOK_PAGE_ID)
    print(data)

    articles = data['data']
    next_link = data['next']

    while next_link:
        data = read_posts(next_link, FACEBOOK_PAGE_ID)
        print(data)
        articles = articles + data['data']
        next_link = data['next']

    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M')
    filename = FACEBOOK_PAGE_ID + '_' + timestamp + '.json'

    with open(filename, 'w') as outfile:
        json.dump(articles, outfile)


if __name__ == '__main__':

    FACEBOOK_PAGE_ID = 'abscbnNEWS'

    ACCESS_TOKEN = 'EAAcBQf4DCosBAFsxJiY9S3EsCFzE8CGG6XpZAgspaSn1gsIyykDgJfPTSvewTS7xJB0CfJuZA6Sc04udH8ZBuvct05h33uADUQM5O7FOeBIyVuqTTGZApOR8qFTmkH7LOc2CB1mV7MZBx29qpJq188BdZAiwyZCVaoZD'

    scrape_page(FACEBOOK_PAGE_ID, ACCESS_TOKEN)