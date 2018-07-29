
from pymongo import MongoClient
import bsoup.scraper.scripts.db_config as config


def init_db(db):
    client = MongoClient(config.host, config.port)
    return client[db]

def insert_row(collection,row):
    key = {'url':row['url']}
    collection.update(key,row,upsert=True)