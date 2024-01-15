# Part 2 of Homework 1: Home Timelines

import os
import pymysql
from tweet_mysql import TweetUserAPI
from tweet_objects import Tweet, User

# Establish a database connection
connection = pymysql.connect(
    host="localhost", user="tweetuser", password="password", db="Tweets"
)

# run and obtain max and min
min_id, max_id = TweetUserAPI.get_min_max_user_id()


def main(min_id, max_id):
    # Authenticate
    api = TweetUserAPI(
        os.environ["TWEET_USER"], os.environ["TWEET_PASSWORD"], "tweetuser"
    )

    # Get timeline for a specific user
    tweets = api.get_random_timeline(min_id, max_id)
    return tweets
