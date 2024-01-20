# Part 1 of Homework 1: Posting Tweets

import csv
import os
import random
import time
from datetime import datetime
from pprint import pprint

import dotenv
import pymysql
from dotenv import dotenv_values, load_dotenv
from pymysql import cursors
from tweet_mysql import TweetUserAPI
from tweet_objects import Tweet

# use working directory
current_dir = os.chdir(os.path.dirname(__file__))

# load environmental variables
# not included in this filepath
load_dotenv()

# Establish a database connection


def get_connection(host, user, password, db):
    """
    Returns a connection object to a MySQL database
    """
    connection = pymysql.connect(
        host=host, user=user, password=password, db=db, cursorclass=cursors.DictCursor
    )
    return connection


def read_tweet_csv(api, csv_data):
    """
    Reads a CSV file and returns a list of Tweet objects

    Args:
        csv_file: A CSV file containing tweet data
    Returns:

        A list of Tweet objects
    """

    for row in csv_data:
        one_tweet = Tweet(int(row["USER_ID"]), row["TWEET_TEXT"], datetime.now())
        api.post_tweet(one_tweet)


def api_tracker(api, call_function, num_iterations=30, per_second=True):
    """
    Tracks the number of API calls made when getting random timelines

    Args:
        api: An instance of TweetUserAPI
        num_timelines: The number of timelines to get
    """

    # Initialize API call counter
    api_calls = 0

    # Record start time
    start_time = time.time()

    # Run get_random_timelines and increment API call counter
    for _ in range(num_iterations):
        api_calls, *values = call_function(
            api_calls=api_calls
        )  # will use the api most likely

    # Record end time
    end_time = time.time()

    # Print total number of API calls and API calls per second
    print(f"Total API calls: {api_calls}")

    if per_second is True:
        # Calculate elapsed time
        elapsed_time = end_time - start_time

        # Calculate API calls per second
        api_calls_per_second = api_calls / elapsed_time

        print(f"API calls per second: {api_calls_per_second}")


def main(csv_file):
    # Open the CSV file once to get the data object,
    # then can get each row with the read_tweet_csv function instead of reading the file each function call
    csv_data = csv.DictReader(open(csv_file))
    # Authenticate
    api = TweetUserAPI(os.getenv("TWEET_USER"), os.getenv("TWEET_PASSWORD"), "Tweets")

    # Load tweets data into sql database one at a time
    api_tracker(api, read_tweet_csv(api, csv_data), num_iterations=1, per_second=False)

    # Get random timelines
    api_tracker(api, api.get_random_timeline(), num_iterations=30, per_second=True)


# Driver Code
if __name__ == "__main__":
    main(csv_file="tweet.csv")  # set filename to tweets to initialize tweets table
