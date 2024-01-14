
import os
from tweet_mysql import TweetUserAPI
from tweet_objects import User, Tweet

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


if __name__ == '__main__':
    main()