import sys
sys.path.insert(0, '.')

import bsoup.scraper.abscbn as abscbn_scraper
import bsoup.scraper.cnn as cnn_scraper

import processor.db.helper as helper
import json

out_data = []

if __name__ == '__main__':


    posts = helper.get_posts('*', source='cnnphilippines')
    posts = [post for post in posts if 'shared_story' in post[1]]

    for post in posts:
        id = post[0]
        url = post[7]
        title = post[2]
        timestamp = post[11]


        data = abscbn_scraper.scrape(url)

        data['post_id'] = id
        data['timestamp'] = timestamp.strftime('%m/%d/%Y %H:%M:%S')
        out_data.append(data)
        print(data)

    with open('out_scraped_cnn.json','w') as outfile:
        json.dump(out_data, outfile, ensure_ascii=True)