SELECT_ALL_FACEBOOK_POSTS = 'SELECT * FROM fb_posts;'

SELECT_ALL_FACEBOOK_POSTS_FIELDS = "SELECT {} from fb_posts WHERE (description REGEXP '[[:<:]]{}[[:>:]]' OR summary REGEXP '[[:<:]]{}[[:>:]]') AND source REGEXP '[[:<:]]{}[[:>:]]' ORDER BY timestamp DESC";

SELECT_FACEBOOK_POSTS_SUMMARY = "SELECT * FROM FB_POSTS WHERE (description REGEXP '[[:<:]]{}[[:>:]]' OR summary REGEXP '[[:<:]]{}[[:>:]]') AND TIMESTAMP >= '{}' AND TIMESTAMP <= '{}' ORDER BY COMMENTS DESC"


SELECT_FACEBOOK_COMMENTS_SUMMARY = "SELECT a.timestamp, b.source, b.thumb_picture, a.message, a.polarity, a.sentiment, a.likes, a.comments, b.permalink_url from fb_comments a join fb_posts b on a.post_id = b.post_id WHERE message REGEXP '[[:<:]]{}[[:>:]]' ORDER BY a.comments desc limit 5000;"

SELECT_ALL_FACEBOOK_COMMENTS = 'SELECT * FROM fb_comments;'


SELECT_QUERY_FACEBOOK_POSTS = "SELECT * FROM fb_posts WHERE description REGEXP '[[:<:]]{}[[:>:]]'or summary REGEXP '[[:<:]]{}[[:>:]]';"

SELECT_QUERY_FACEBOOK_COMMENTS = "SELECT * FROM fb_comments WHERE message REGEXP '[[:<:]]{}[[:>:]]';"

SELECT_COMMENTS_BY_POSTS = "SELECT a.summary, b.* from fb_posts a join fb_comments b where a.post_id = b.post_id and b.post_id IN (SELECT post_id from fb_posts where summary REGEXP '[[:<:]]{}[[:>:]]');"

SELECT_TIME_AGGREGATED_FACEBOOK_POSTS = "SELECT YEAR(timestamp), MONTH(timestamp), DAY(timestamp), count(*) AS COUNT FROM fb_posts  WHERE description like '%{}%' GROUP BY YEAR(timestamp), MONTH(timestamp), DAY(timestamp)"

SELECT_TIME_AGGREGATED_FACEBOOK_COMMENTS = "SELECT YEAR(timestamp), MONTH(timestamp), DAY(timestamp), sentiment, count(*) AS COUNT FROM fb_comments  WHERE sentiment is not null and message like '%{}%' GROUP BY YEAR(timestamp), MONTH(timestamp), DAY(timestamp),sentiment"

SELECT_POST_IDS_PREV_MONTH = 'SELECT post_id from fb_posts where timestamp >= (SELECT DATE_FORMAT(DATE_SUB(NOW(), INTERVAL 30 day), "%Y-%m-%d")) ORDER BY timestamp DESC;'

def select_query_facebook_posts(term):
    return SELECT_QUERY_FACEBOOK_POSTS.format(term,term)

def select_query_facebook_comments(term):
    return SELECT_QUERY_FACEBOOK_COMMENTS.format(term)

def select_all_facebook_posts():
    return SELECT_ALL_FACEBOOK_POSTS

def select_all_facebook_comments():
    return SELECT_ALL_FACEBOOK_COMMENTS

def select_comments_by_posts(term):
    return SELECT_COMMENTS_BY_POSTS.format(term)

# Posts aggregated by time
def select_time_aggregated_facebook_posts(term):
    return SELECT_TIME_AGGREGATED_FACEBOOK_POSTS.format(term)

# Comments aggregated by time and sentiment
def select_time_aggregated_facebook_comments(term):
    return SELECT_TIME_AGGREGATED_FACEBOOK_COMMENTS.format(term)