# Script to read Facebook Page posts using Facebook Graph API
# Input
# @ FACEBOOK_PAGE_ID
# @ ACCESS TOKEN - valid and not expired


import requests
import json
import processor.db.helper as helper

def get_comments(post_id, url):

    next_url = url

    while next_url is not '':
        print('URL: {}'.format(next_url))

        try:
            url_content = requests.get(next_url,verify=False).json()
        except Exception:
            next_url = ''
            continue

        # print(content)

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

            sub_comments = comment.get('comments')

            if comment.get('comments'): del comment['comments']
            del comment['id']

            helper.insert_facebook_comment(comment)

            while sub_comments:
                for sub_comment in sub_comments['data']:
                    print(sub_comment)

                    sub_comment['post_id'] = post_id
                    sub_comment['comment_id'] = sub_comment['id']
                    sub_comment['parent_comment_id'] = comment['comment_id']
                    helper.insert_facebook_comment(sub_comment)

                # Loop through the next subcomments
                if 'next' in sub_comments['paging']:
                    next_sub_url = sub_comments['paging']['next']
                    try:
                        sub_comments = requests.get(next_sub_url, verify=False).json()
                    except:
                        break
                    print('next!')

                else:
                    sub_comments = None # No more comments retrieved. Return.


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

    post_ids = list(helper.get_posts(['post_id'], '*'))

    ACCESS_TOKEN = 'EAAcBQf4DCosBAFsxJiY9S3EsCFzE8CGG6XpZAgspaSn1gsIyykDgJfPTSvewTS7xJB0CfJuZA6Sc04udH8ZBuvct05h33uADUQM5O7FOeBIyVuqTTGZApOR8qFTmkH7LOc2CB1mV7MZBx29qpJq188BdZAiwyZCVaoZD'

    print(len(post_ids))

    comments = scrape_comments(post_ids, ACCESS_TOKEN)
