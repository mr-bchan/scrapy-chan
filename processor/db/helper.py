from processor.db.mysql_db import Database
import processor.db.query_builder as query_builder
import processor.db.db_config as db_config

import requests
import json

db = Database(db_config.DB_HOST, db_config.DB_USER, db_config.DB_PWD, db_config.DB_DB)

def get_posts(fields, term='*',source='*'):
    return db.query_row(query_builder.SELECT_ALL_FACEBOOK_POSTS_FIELDS.format(','.join(fields), term, term, source))

def get_sentiment(text):
    try:
        myurl = "http://neuralmechanics.ai/analitika/nlp/sentiment/"
        body = {'data': text}
        response = requests.post(myurl, auth=('nmdev', 'nmdev'), verify=True, json=body)
        response = json.loads(response.content)
        return response['data']['polarity']

    except Exception:
        return 0


def get_entities(text):
    myurl = "http://neuralmechanics.ai/analitika/nlp/ner/"
    body = {'data': text}
    response = requests.post(myurl, auth=('nmdev', 'nmdev'), verify=True, json=body)
    response = json.loads(response.content)

    if response['success']:
        return response['data']['entities']
    else:
        return {}

def insert_facebook_post(post):
    try:
        #
        # print(post['description'])
        # entities = get_entities(post['description'])
        # print(entities)
        #
        db.insert_facebook_post([
            post['id'],
            post['type'],
            post['title'],
            post['summary'],
            post['description'],
            post['source'],
            post['link'],
            post['comments'],
            post['likes'],
            post['shares'],
            post['timestamp']
        ])
    except UnicodeEncodeError:
        print('Error encountered while inserting row (Unicode)')


def insert_facebook_comment(comment):
    try:
        if 'post_id' in comment:

            # entities = get_entities(comment['message'])
            # print(entities)
            comment['message'] = comment['message']
            polarity = get_sentiment(comment['message'].encode('unicode-escape'))
            print('Compute polarity: {}'.format(polarity))
            if polarity < 0:
                sentiment = 'negative'
            elif polarity <= 0.5:
                sentiment = 'neutral'
            else:
                sentiment = 'positive'

            db.insert_facebook_comment([
                comment['post_id'],
                comment['comment_id'],
                comment['created_time'],
                comment['message'],
                comment['like_count'],
                comment['comment_count'],
                comment['parent_comment_id'],
                sentiment,
                polarity
            ])
    except UnicodeEncodeError:
        print('Error encountered while inserting row (Unicode)')


def get_posts_time_aggregated(text):
        query = query_builder.select_time_aggregated_facebook_posts(text)
        result = list(db.query_row(query))
        return result


def get_comments_time_aggregated(text):
    query = query_builder.select_time_aggregated_facebook_comments(text)
    result = list(db.query_row(query))
    return result

if __name__ == '__main__':

    folder = '../../results'

    files = [
            'rapplerdotcom_20180521_1950.json',
             'inquirerdotnet_20180521_1947.json',
             'gmanewstv_20180521_1945.json',
             'CNNPhilippines_20180521_1943.json',
             'abscbnNEWS_20180521_1941.json',
             'gmanews_20180521_2153.json']

    for file in files:
        with open(folder + '/comments_' + file) as json_data:
            data = json.load(json_data)

        sereno_comments = [post for post in data if 'sereno' in post['message'].lower()]
        print(len(sereno_comments))
        for post in sereno_comments:
            insert_facebook_comment(post)

    # posts = db.query_row(query_builder.select_query_facebook_posts('sereno'))

    # comments = db.query_row(query_builder.select_query_facebook_comments('sereno'))
    #
    # text = [[comment[1], comment[3]] for comment in comments if comment[3] is not '']
    # # print(text)
    #
    # import csv
    #
    # myFile = open('sereno_comments.csv', 'w')
    # with myFile:
    #     writer = csv.writer(myFile)
    #     writer.writerows(text)
    #
    # print("Writing complete")
    #
    # # post_comments = db.query_row(query_builder.select_comments_by_posts('sereno'))
