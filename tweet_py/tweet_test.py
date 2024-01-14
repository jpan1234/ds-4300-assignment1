
import os
from tweet_mysql import TweetUserAPI
from tweet_objects import User, Tweet
import csv


"""
def main():

    # Authenticate
    api = TweetUserAPI(os.environ["TWEET_USER"], os.environ["TWEET_PASSWORD"], "tweetuser")

    # Get tweets from a specific user
    tweets = api.get_user_tweets("userid")
    for t in tweets:
        print(t)

    # Post a new tweet
    tweet = Tweet("userid", "This is a new tweet.", "2022-01-01 00:00:00")
    api.post_tweet(tweet)
"""


def load_csv_file(api, filename):

    # open the file
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            follows = Follows(*row)
            sql = "INSERT INTO FOLLOWS (user_id, follows_id) VALUES (%s, %s)"
            api.dbu.insert_one(sql, (follows.user_id, follows.follows_id))

# In your main function
def main():
    # Authenticate
    api = TweetUserAPI(os.environ["TWEET_USER"], os.environ["TWEET_PASSWORD"], "tweetuser")

    # Load follows data
    load_csv_file(api, 'follows.csv')

    # Rest of your code...

if __name__ == '__main__':
    main()