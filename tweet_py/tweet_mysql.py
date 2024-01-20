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

    def post_tweet(self, tweet, api_calls=None, track=True):
        """
        This method takes a Tweet object as an argument and inserts a new record into the
        tweet table in the database. It constructs an SQL INSERT statement and uses the
        insert_one method of the DBUtils instance to execute it.
        """

        if track and api_calls is None:
            api_calls = 0

        # Get the current date and time
        if tweet.tweet_ts is None:
            tweet.tweet_ts = datetime.now()

        # insert SQL statement
        sql = "INSERT INTO TWEETS (user_id, tweet_text, tweet_ts) VALUES (%s, %s, %s)"
        # values of the tweet
        val = (tweet.user_id, tweet.tweet_text, tweet.tweet_ts)
        # insert using insert_one method
        self.dbu.insert_one(sql, val)
        # update the tracker
        if track:
            api_calls += 1
            return api_calls

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

        sql = f""" CALL get_timeline({user_id}); """

        # create the dataframe
        df = self.dbu.execute(sql)

        timeline = [Tweet(*df.iloc[i]) for i in range(len(df))]
        # return the timeline
        return timeline

    def get_user_ids(self):
        """
        Gets all user_ids from the Tweets table

        Returns:
            A list of user_ids
        """

        # get distinct user_ids from Tweets table
        sql = "SELECT DISTINCT user_id FROM Tweets;"
        df = self.dbu.execute(sql)

        return df["user_id"].tolist()

    def get_random_timeline(self, api_calls=None, track=True):
        """
        Gets a number of timelines for random users

        Args:
            api: An instance of TweetUserAPI
            num_timelines: The number of timelines to get
        """
        if track and api_calls is None:
            api_calls = 0

        # get user_ids
        user_ids = self.get_user_ids()

        # Run get_timeline num_timelines times with a random user_id
        # select a random choice
        user_id = random.choice(user_ids)

        # obtain timeline
        timeline = self.get_timeline(user_id)

        # unpack the timeline and print it
        unpacked_timeline = [(tweet.user_id, tweet.tweet_text) for tweet in timeline]

        if track:
            api_calls += 1
            print(f"Timeline for user_id {user_id}: {unpacked_timeline}")
            return api_calls
        else:
            return print(f"Timeline for user_id {user_id}: {unpacked_timeline}")
