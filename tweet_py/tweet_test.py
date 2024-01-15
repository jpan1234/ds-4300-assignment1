
import os
from tweet_mysql import TweetUserAPI
from tweet_objects import User, Tweet
import csv
import pymysql 


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

# Establish a database connection
connection = pymysql.connect(host='localhost',
                             user='tweetuser',
                             password='password',
                             db='Tweets')

try:
    with connection.cursor() as cursor:
        print(cursor)
        # Open the CSV file
        with open('hw1_data/follows.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip the header row
            for row in csv_reader:
                # Insert each row into the Follows table
                sql = "INSERT INTO Follows (user_id, follows_id) VALUES (%s, %s)"
                cursor.execute(sql, row)

    # Commit the changes
    connection.commit()

finally:
    # Close the database connection
    connection.close()
"""
# Driver Code 
if __name__ == "__main__" : 
    mysqlconnect()
"""
"""
# In your main function
def main():
    # Authenticate
    api = TweetUserAPI(os.environ["TWEET_USER"], os.environ["TWEET_PASSWORD"], "tweetuser")

    # Load follows data
    load_csv_file(api, 'follows.csv')

    # Rest of your code...

if __name__ == '__main__':
    main()

"""