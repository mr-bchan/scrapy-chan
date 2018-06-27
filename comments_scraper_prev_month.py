import key_config as config
import processor.db.helper as helper
import comments_scraper
if __name__ == '__main__':

    post_ids = list(helper.get_post_ids_prev_month())
    print(len(post_ids))
    comments = comments_scraper.scrape_comments(post_ids, config.ACCESS_TOKEN)
