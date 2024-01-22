# Part 1 of Homework 1: Posting Tweets

import csv
import os

from datetime import datetime

from dotenv import load_dotenv
from tweet_mysql import TweetUserAPI
from tweet_objects import Tweet

# use working directory
current_dir = os.chdir(os.path.dirname(__file__))

# load environmental variables
# not included in this filepath
load_dotenv()


def read_tweet_csv(api, csv_data, track=True):
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

    if track:
        print(f"Number of API calls per second: {api.post_tweet.calls_per_second}")


def main(csv_file):
    # Open the CSV file once to get the data object,
    # then can get each row with the read_tweet_csv function instead of reading the file each function call
    csv_data = csv.DictReader(open(csv_file))
    # Authenticate
    api = TweetUserAPI(os.getenv("TWEET_USER"), os.getenv("TWEET_PASSWORD"), "Tweets")
    # Load tweets data into sql database one at a time
    read_tweet_csv(api, csv_data)
    api.get_random_timelines(30, track=True)


# Driver Code
if __name__ == "__main__":
    main(csv_file="tweet.csv")  # set filename to tweets to initialize tweets table
