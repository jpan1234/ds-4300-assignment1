"""
Tweet-User Database API for MySQL
"""

import random
from datetime import datetime
from tweet_dbutils import DBUtils
from tweet_objects import Follows, Tweet


class TweetUserAPI:
    def __init__(self, user, password, database, host="localhost"):
        self.dbu = DBUtils(user, password, database, host)

    def post_tweet(self, tweet):
        """
        This method takes a Tweet object as an argument and inserts a new record into the
        tweet table in the database. It constructs an SQL INSERT statement and uses the
        insert_one method of the DBUtils instance to execute it.
        """

    

        # Get the current date and time
        current_timestamp = datetime.now()

        print(current_timestamp)

        # insert SQL statement
        sql = "INSERT INTO TWEETS (user_id, tweet_text, tweet_ts) VALUES (%s, %s, %s)"
        # values of the tweet
        val = (tweet.user_id, tweet.tweet_text, tweet.current_timestamp)
        # insert using insert_one method
        self.dbu.insert_one(sql, val)

    def get_followees(self, user_id):
        # obtain the followees
        sql = """
                SELECT F.follows_id
                FROM Follows as F
                LEFT JOIN Tweets T ON F.user_id = T.user_id
                WHERE T.user_id = %s"""

        # create the dataframe
        df = self.dbu.execute(sql, user_id)  # type:ignore
        followees = [Follows(*df.iloc[i]) for i in range(len(df))]
        # return the followees
        return user_id, followees

    def get_following_count(self, user_id):
        # obtain the followees
        sql = """
                SELECT COUNT(F.follows_id) AS following_count
                FROM Follows as F
                LEFT JOIN Tweets T ON F.user_id = T.user_id
                WHERE T.user_id = %s"""

        # create the dataframe
        df = self.dbu.execute(sql, user_id)  # type:ignore
        following_count = df.iloc[0]["following_count"]
        # return the followees
        return following_count

    def get_timeline(self, user_id):
        """
        This method takes a user_id as an argument and returns a list of Tweet objects
        posted by the specified user. It constructs an SQL SELECT statement and
        uses the execute method of the DBUtils instance to execute it. The returned data frame
        is then used to create a list of Tweet objects.
        """
        # obtain the tweets
        sql = f"""
            SELECT DISTINCT F.follows_id, T.tweet_text, T.tweet_ts
            FROM Follows F
            INNER JOIN Tweets T on F.follows_id = T.user_id
            WHERE F.follows_id IN (SELECT follows_id FROM Follows WHERE user_id = {user_id})
            AND F.user_id = {user_id}
            ORDER BY T.tweet_ts DESC
            LIMIT 10;
            """

        # create the dataframe
        df = self.dbu.execute(sql, user_id)
        timeline = [Tweet(*df.iloc[i]) for i in range(len(df))]
        # return the timeline
        return timeline


    def get_user_ids(self):
        """
        Gets all user_ids from the Tweets table

        Returns:
            A list of user_ids
        """

        sql = "SELECT DISTINCT user_id FROM Tweets;"
        df = self.dbu.execute(sql)

        return df['user_id'].tolist()


