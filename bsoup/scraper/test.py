import sys
sys.path.insert(0, '.')

import bsoup.scraper.abscbn as abscbn_scraper
import processor.db.helper as helper
import json

abscbn_data = []

if __name__ == '__main__':
    posts = helper.get_posts('*', source='abscbnnews')
    posts = [post for post in posts if 'news.abs-cbn.com' in post[7]]

    for post in posts:
        id = post[0]
        url = post[7]
        title = post[2]
        timestamp = post[11]

        data = abscbn_scraper.scrape(url)

        data['post_id'] = id
        data['timestamp'] = timestamp.strftime('%m/%d/%Y %H:%M:%S')
        abscbn_data.append(data)

    with open('out_scraped_abscbn.json','w') as outfile:
        json.dump(abscbn_data, outfile, ensure_ascii=True)