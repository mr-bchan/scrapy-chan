import requests

def scrape_page(POST_ID, ACCESS_TOKEN):
    URL = 'https://graph.facebook.com/v2.12/' + POST_ID +\
          '?fields=' \
          'id,created_time,message,attachments,link,permalink_url,shares,%20status_type,%20comments.limit(0).summary(true),reactions.type(LIKE).summary(total_count).as(like),reactions.type(LOVE).summary(total_count).as(love),reactions.type(HAHA).summary(total_count).as(haha),reactions.type(WOW).summary(total_count).as(wow),reactions.type(SAD).summary(total_count).as(sad),reactions.type(ANGRY).summary(total_count).as(angry)&access_token=' + ACCESS_TOKEN + '&pretty=0;'

    url_content = requests.get(URL, verify=False).json()


    if 'error' not in url_content:
        print(url_content)

    else:
        print(url_content['error'])

if __name__ == '__main__':

    FACEBOOK_PAGE_ID = 27254475167
    POST_SEED = 1000000000

    import time
    import datetime

    start_date = "06/01/2018"
    end_date = "06/02/2018"

    start_unix_time = int(time.mktime(datetime.datetime.strptime(start_date, "%m/%d/%Y").timetuple()))
    end_unix_time = int(time.mktime(datetime.datetime.strptime(end_date, "%m/%d/%Y").timetuple()))

    print(start_unix_time)
    print(end_unix_time)

    ACCESS_TOKEN = 'EAAcBQf4DCosBAFsxJiY9S3EsCFzE8CGG6XpZAgspaSn1gsIyykDgJfPTSvewTS7xJB0CfJuZA6Sc04udH8ZBuvct05h33uADUQM5O7FOeBIyVuqTTGZApOR8qFTmkH7LOc2CB1mV7MZBx29qpJq188BdZAiwyZCVaoZD'

    while POST_SEED < 10156278149450168:
        POST_ID = "{}_{}".format(FACEBOOK_PAGE_ID, POST_SEED)
        scrape_page(POST_ID, ACCESS_TOKEN)
        POST_SEED = POST_SEED + 1

