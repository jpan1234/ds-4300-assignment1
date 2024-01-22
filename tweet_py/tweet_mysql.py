"""
Tweet-User Database API for MySQL
"""

import random
import time

from tweet_dbutils import DBUtils
from tweet_objects import Follows, Tweet


def count_calls(func):
    """
    Decorator function to count API calls
    """

    def wrapper(*args, **kwargs):
        # Record the start time on the first call
        if wrapper.calls == 0:
            wrapper.start_time = time.time()

        # Increment the number of calls
        wrapper.calls += 1

        # Calculate the elapsed time and calls per second
        elapsed_time = time.time() - wrapper.start_time
        if elapsed_time != 0:
            wrapper.calls_per_second = wrapper.calls / elapsed_time
        else:
            wrapper.calls_per_second = wrapper.calls  # Or some other value

        # Call the function being decorated
        return func(*args, **kwargs)

    # Initialize counter and start time
    wrapper.calls = 0
    wrapper.start_time = None
    wrapper.calls_per_second = None
    return wrapper


class TweetUserAPI:
    def __init__(self, user, password, database, host="localhost"):
        self.dbu = DBUtils(user, password, database, host)

    @count_calls
    def post_tweet(self, tweet):
        """
        This method takes a Tweet object as an argument and inserts a new record into the
        tweet table in the database. It constructs an SQL INSERT statement and uses the
        insert_one method of the DBUtils instance to execute it.
        """

        # insert SQL statement
        sql = "INSERT INTO TWEETS (user_id, tweet_text, tweet_ts) VALUES (%s, %s, %s)"
        # values of the tweet
        val = (tweet.user_id, tweet.tweet_text, tweet.tweet_ts)
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

    @count_calls
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

    def get_random_timelines(self, num_timelines, track=False):
        """
        Gets a number of timelines for random users

        Args:
            api: An instance of TweetUserAPI
            num_timelines: The number of timelines to get
        """
        for i in range(num_timelines):
            # get user_ids
            user_ids = self.get_user_ids()

            # Run get_timeline num_timelines times with a random user_id
            # select a random choice
            user_id = random.choice(user_ids)

            # obtain timeline
            timeline = self.get_timeline(user_id)

            # unpack the timeline and print it
            unpacked_timeline = [
                (tweet.user_id, tweet.tweet_text) for tweet in timeline
            ]

            print(f"Timeline for user_id {user_id}: {unpacked_timeline}")

        if track:
            return print(f"API calls per second: {self.get_timeline.calls_per_second}")
