"""
Tweet-User Database API for MySQL
"""

import random

from tweet_dbutils import DBUtils
from tweet_objects import Follows, Tweet


class TweetUserAPI:
    def __init__(self, user, password, database, host="localhost"):
        self.dbu = DBUtils(user, password, database, host)
        # self.dbu.create_indices(column="USER_ID", table="Tweets")
        # self.dbu.create_indices(column="TWEET_TEXT", table="Tweets")
        # self.dbu.create_indices(column="FOLLOWS_ID", table="Follows")
        # self.dbu.create_indices(column="USER_ID", table="Follows")

    def post_tweet(self, tweet):
        """
        This method takes a Tweet object as an argument and inserts a new record into the
        tweet table in the database. It constructs an SQL INSERT statement and uses the
        insert_one method of the DBUtils instance to execute it.
        """
        # insert SQL statement
        sql = "INSERT INTO TWEETS (user_id, tweet_text) VALUES (%s, %s)"
        # values of the tweet
        val = (tweet.user_id, tweet.tweet_text)
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
            SELECT T.tweet_id, T.user_id, T.tweet_ts, T.tweet_text
            FROM Tweets T
            INNER JOIN Follows F ON T.user_id = F.follows_id
            WHERE T.user_id = {user_id}
            ORDER BY T.tweet_ts DESC
            LIMIT 10"""

        # create the dataframe
<<<<<<< HEAD
        df = self.dbu.execute(sql, user_id)
=======
        df = self.dbu.execute(sql)  
>>>>>>> 4a2c468661731faead6f1ced239b539e56661e7b
        timeline = [Tweet(*df.iloc[i]) for i in range(len(df))]
        # return the timeline
        return timeline


def get_min_max_user_id():
    """
    This function retrieves the minimum and maximum user_id from the users table in the database.

    Returns:
    tuple: A tuple containing the minimum and maximum user_id.
    """
    # Connect to the database
    conn = your_database_connection()

    # Get the min and max user_id
    cursor = conn.cursor()
    cursor.execute("SELECT MIN(user_id), MAX(user_id) FROM users")
    min_id, max_id = cursor.fetchone()

    return min_id, max_id


def get_random_user_timeline(self,max_id, min_id=1):
    """
    This function retrieves the timeline for a random user.

    Returns:
    list: A list of Tweet objects representing the timeline for a random user.
    """
    # Generate a random user_id
    random_id = random.randint(min_id, max_id)

    # Get the timeline for the random user
    timeline = get_timeline(random_id)

    return timeline
