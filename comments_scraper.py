# Script to read Facebook Page posts using Facebook Graph API
# Input
# @ FACEBOOK_PAGE_ID
# @ ACCESS TOKEN - valid and not expired

from bsoup import article_scraper as scraper
import requests
import json
import datetime
import time

def get_comments(post_id, url):

    next_url = url
    comments = []

    while next_url is not '':
        print('URL: {}'.format(next_url))
        url_content = requests.get(next_url).json()
        # print(content)

        if 'comments' not in url_content and 'data' in url_content:
            content = url_content
        elif 'comments' in url_content:
            content = url_content['comments']
        else:
            print('No comments found for: {}'.format(post_id))
            print(url_content)
            return {'data':comments}

        print('Number of comments: ' + str(len(content['data'])))

        for comment in content['data']:
            comment['post_id'] = post_id
            comment['comment_id'] = comment['id']
            comment['parent_comment_id'] = ""

            sub_comments = comment.get('comments')

            if comment.get('comments'): del comment['comments']
            del comment['id']

            comments.append(comment)

            if sub_comments:
                for sub_comment in sub_comments['data']:
                    sub_comment['post_id'] = post_id
                    sub_comment['comment_id'] = sub_comment['id']
                    sub_comment['parent_comment_id'] = comment['comment_id']
                    del sub_comment['id']
                    comments.append(sub_comment)


            try: next_url = content['paging']['next']
            except Exception: next_url = ''

        # print(comments)


    return {'data':comments}


def scrape_comments(posts, ACCESS_TOKEN):

    comments = []

    for post_id in posts:
        URL = 'https://graph.facebook.com/v3.0/' + post_id +\
             '?fields=comments.limit(100){id, created_time, message, like_count, comment_count, comments{id, created_time, message, like_count, comment_count}}' \
             '&access_token='+ACCESS_TOKEN

        comment_list = get_comments(post_id, URL)['data']
        comments = comments + comment_list

    return comments

if __name__ == '__main__':

    json_file = 'abscbnNEWS_20180518_1006.json'

    with open(json_file) as json_data:
        data = json.load(json_data)

    len(data)
    data[5550]
    id_set = [d['id'] for d in data]

    ACCESS_TOKEN = 'EAAcBQf4DCosBAFsxJiY9S3EsCFzE8CGG6XpZAgspaSn1gsIyykDgJfPTSvewTS7xJB0CfJuZA6Sc04udH8ZBuvct05h33uADUQM5O7FOeBIyVuqTTGZApOR8qFTmkH7LOc2CB1mV7MZBx29qpJq188BdZAiwyZCVaoZD'

    comments = scrape_comments(id_set, ACCESS_TOKEN)

    FILENAME = json_file.split('/')[1]

    filename = 'comments_' + FILENAME

    with open(filename, 'w') as outfile:
        json.dump(comments, outfile)