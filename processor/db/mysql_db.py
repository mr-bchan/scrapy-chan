import MySQLdb


class Database:
    def __init__(self, port, user, password ,db):

        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.conn = MySQLdb.connect(self.port, self.user, self.password, self.db)
        self.cursor = self.conn.cursor()

        self.FB_POST_TABLE = 'fb_posts'
        self.FB_COMMENT_TABLE = 'fb_comments'

        print('*******************')
        print('MySQL up in {}:{} db: {}'.format(port,user,db))
        print('*******************')

    def insert_row(self, query, on_duplicate_keys):
        try:
            query = query + ' ON DUPLICATE KEY UPDATE ' + on_duplicate_keys

            print(query)
            self.cursor.execute(query)
            self.conn.commit()

        except Exception as e:
            print('Error encountered')
            print(e)

            # Ping to establish new conection
            self.conn.ping(True)
            self.insert_row(query, on_duplicate_keys)

    def query_row(self, query):
       try:
           print(query)

           self.conn.ping(True)
           print('***')
           self.cursor.execute(query)
           self.conn.commit()

           # Execute the SQL command
           self.cursor.execute(query)

           # Fetch all the rows in a list of lists.
           results = self.cursor.fetchall()

           print('Number of rows retrieved: {}').format(len(results))

           return results

       except Exception as e:
           print('Error encountered')
           print(e)
           self.conn.ping(True)
           self.query_row(query)

    # Query to insert facebook posts
    def insert_facebook_post(self, row):

        print(row)
        keys = ['type','title','summary','description','source','tags','link','comments','likes','shares','timestamp']

        post_id = row[0]
        type = row[1]
        title = str(row[2].encode('utf-8').replace('"','').replace('\'',""))
        summary = str(row[3].encode('utf-8').replace('"',''))
        description = str(row[4].encode('utf-8').replace('"',''))
        source = row[5]
        tags = ""
        link = row[6]
        comments = row[7]
        likes = row[8]
        shares = row[9]

        # Timestamp needs to be converted to a format
        timestamp = row[10].replace('T', ' ')[:-5]

        #print(formatted_timestamp)
        query = 'INSERT INTO {} VALUES ("{}", "{}", "{}", "{}", "{}","{}","{}","{}",{},{},{},"{}")'\
            .format (self.FB_POST_TABLE, post_id, type, title, summary, description, source, tags, link, comments, likes, shares, timestamp)

        self.insert_row(query=query, on_duplicate_keys=self.create_on_duplicate_query(keys))

        #print('entities:')
        #print(self.get_entities(summary))

    # Query to insert facebook comments
    def insert_facebook_comment(self, row):

        keys = ['timestamp','message','likes','comments','parent_comment_id','sentiment','polarity']

        post_id = row[0]
        comment_id = row[1]

        # Timestamp needs to be converted to a format
        timestamp = row[2].replace('T', ' ')[:-5]

        message = str(row[3].encode('utf-8').replace('"','').replace('\'',""))
        likes = row[4]
        comments = row[5]
        parent_comment_id = row[6]

        sentiment = row[7]
        polarity = row[8]

        #print(formatted_timestamp)
        query = 'INSERT INTO {} VALUES ("{}", "{}", "{}", "{}", {},{},"{}","{}",{})'\
            .format (self.FB_COMMENT_TABLE, post_id, comment_id, timestamp, message, likes, comments, parent_comment_id, sentiment, polarity)

        self.insert_row(query=query, on_duplicate_keys=self.create_on_duplicate_query(keys))

    def create_on_duplicate_query(self, keys):
        # maps key list to key = VALUES(key) format
        return ','.join(list(map(lambda k:  k + ' = VALUES(' + k + ')', keys)))

