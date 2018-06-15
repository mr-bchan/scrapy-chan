# Script to read Facebook Page posts using Facebook Graph API
# Input
# @ FACEBOOK_PAGE_ID
# @ ACCESS TOKEN - valid and not expired


import requests
import json
import processor.db.helper as helper
import key_config as config


def get_comments(post_id, url):

    next_url = url
    comment_ctr = 0

    while next_url is not '' and comment_ctr < 10000:
        print('URL: {}'.format(next_url))
        try:
            url_content = requests.get(next_url,verify=False).json()
        except Exception:
            next_url = ''
            continue

        if 'comments' not in url_content and 'data' in url_content and len(url_content['data']) > 0:
            content = url_content
        elif 'comments' in url_content and len(url_content['comments']['data']) > 0:
            content = url_content['comments']
        else:
            print('No comments found for: {}'.format(post_id))
            print(url_content)
            return

        print('Number of comments: ' + str(len(content['data'])))

        for comment in content['data']:
            comment['post_id'] = post_id
            comment['comment_id'] = comment['id']
            comment['parent_comment_id'] = ""

            if comment.get('comments'): del comment['comments']
            del comment['id']

            helper.insert_facebook_comment(comment)
            comment_ctr = comment_ctr + 1

            try: next_url = content['paging']['next']
            except Exception: next_url = ''


def scrape_comments(posts, ACCESS_TOKEN):

    for idx,post_id in enumerate(posts):
        post_id = post_id[0]
        print('\nProcessing {} out of {} posts'.format(idx + 1, len(posts)))

        URL = 'https://graph.facebook.com/v3.0/' + post_id +\
             '?fields=comments.limit(100){id, created_time, message, like_count, comment_count, comments.limit(100){id, created_time, message, like_count, comment_count}}' \
             '&access_token='+ACCESS_TOKEN

        get_comments(post_id, URL)

if __name__ == '__main__':

    post_ids = list(helper.get_posts(['post_id'], '*', '*'))
    print(len(post_ids))
    comments = scrape_comments(post_ids, config.ACCESS_TOKEN)
