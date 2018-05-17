# Script to read Facebook Page posts using Facebook Graph API
# Input
# @ FACEBOOK_PAGE_ID
# @ ACCESS TOKEN - valid and not expired

from bsoup import article_scraper as scraper
import requests
import json
import datetime
import time

def get_comments(url):
    print('URL: {}'.format(url))
    content = requests.get(url).json()

    return {'data':content}


def scrape_comments(posts, ACCESS_TOKEN):

    comments = []

    for post in posts:
        URL = 'https://graph.facebook.com/v2.12/' + post +\
              '?fields=comments.limit(100){id,created_time, message, like_count, comments.limit(100), comment_count}' \
              '&access_token='+ACCESS_TOKEN

        comment_list = get_comments(URL)['data']['comments']

        comments = comments + comment_list

    return comments

if __name__ == '__main__':

    json_file = 'results/abscbnNEWS_20180517_0344.json'

    with open(json_file) as json_data:
        data = json.load(json_data)

    id_set = [d['id'] for d in data]

    ACCESS_TOKEN = 'EAAcBQf4DCosBAFsxJiY9S3EsCFzE8CGG6XpZAgspaSn1gsIyykDgJfPTSvewTS7xJB0CfJuZA6Sc04udH8ZBuvct05h33uADUQM5O7FOeBIyVuqTTGZApOR8qFTmkH7LOc2CB1mV7MZBx29qpJq188BdZAiwyZCVaoZD'

    comments = scrape_comments(id_set, ACCESS_TOKEN)

    FILENAME = json_file.split('/')[1]

    filename = 'comments_' + FILENAME + '.json'

    with open(filename, 'w') as outfile:
        json.dump(comments, outfile)