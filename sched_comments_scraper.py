import key_config as config
import processor.db.helper as helper
import comments_scraper
import sys

if __name__ == '__main__':

    day_interval = sys.argv[1]
    post_ids = list(helper.get_post_ids_prev_month(day_interval=day_interval))
    print(len(post_ids))
    comments = comments_scraper.scrape_comments(post_ids, config.ACCESS_TOKEN)
