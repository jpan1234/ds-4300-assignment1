"""
Tweet-User Database API for MySQL
"""

from dbutils import DBUtils
from tweet_objects import User, Tweet

class TweetUserAPI:

    def __init__(self, user, password, database, host="localhost"):
        self.dbu = DBUtils(user, password, database, host)

    def post_tweet(self, tweet):
        """
        This method takes a Tweet object as an argument and inserts a new record into the 
        tweet table in the database. It constructs an SQL INSERT statement and uses the 
        insert_one method of the DBUtils instance to execute it.
        """
        # insert SQL statement
        sql = "INSERT INTO tweet (username, content, timestamp) VALUES (%s, %s, %s) "
        # values of the tweet
        val = (tweet.user, tweet.content, tweet.timestamp)
        # insert usinig insert_one method
        self.dbu.insert_one(sql, val)

    def get_user_tweets(self, username):
        """
        This method takes a username as an argument and returns a list of Tweet objects 
        posted by the specified user. It constructs an SQL SELECT statement and 
        uses the execute method of the DBUtils instance to execute it. The returned data frame 
        is then used to create a list of Tweet objects.
        """
        # obtain the tweets
        sql = """
                SELECT tweet_id, username, content, timestamp
                FROM tweet
                WHERE username = '""" + username + """'
                ORDER BY timestamp DESC
                LIMIT 10"""
        
        # create the dataframe
        df = self.dbu.execute(sql)
        tweets = [Tweet(*df.iloc[i][1:]) for i in range(len(df))]
        # return the tweets 
        return tweets