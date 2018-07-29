import sys
sys.path.insert(0,'.')

import os
import bsoup.scraper.rappler as scraper
import bsoup.scraper.scripts.db_helper as db_helper
# Input folder name

FOLDER_PATH = '/Users/jay'
DATA_FOLDER = '/news'
SOURCE = 'http://news.abs-cbn.com'

input_html_files = []
for path, subdirs, files in os.walk(FOLDER_PATH + DATA_FOLDER):
    for name in files:
        input_html_files.append(os.path.join(path, name))

for idx,file in enumerate(input_html_files):
    with open(file, 'r') as infile:
        html_text = infile.read()
        output = scraper.parse_body(html_text, file.replace(FOLDER_PATH, SOURCE).replace('.html', ''))

        if output != {}:
            print("{} of {} file scraped".format(idx, len(input_html_files)))

            if output['images'] != []:
                print(output)

            # save to mongodb
            db = db_helper.init_db('censei')
            db_helper.insert_row(db['scraped_links'], output)
