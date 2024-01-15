import csv
import os

import pymysql
from tweet_mysql import TweetUserAPI
from tweet_objects import Tweet, User

# Establish a database connection
connection = pymysql.connect(
    host="localhost", user="tweetuser", password="password", db="Tweets"
)


def main(csv_file):
    # Open the CSV file once to get the data object,
    # then can get each row with the read_tweet_csv function instead of reading the file each function call
    csv_data = csv.DictReader(open(csv_file))
    # Authenticate
    api = TweetUserAPI(
        os.environ["TWEET_USER"], os.environ["TWEET_PASSWORD"], "tweetuser"
    )

    # Load tweets data into sql database one at a time
    read_tweet_csv(api, csv_data)

    # Get timeline for a specific user
    tweets = api.get_timeline("userid")
    for t in tweets:
        print(t)


"""
inserting into follows table
"""
try:
    with connection.cursor() as cursor:
        print(cursor)
        # Open the CSV file
        with open("hw1_data/follows.csv", "r") as file:
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


def read_tweet_csv(api, csv_data):
    """
    Reads a CSV file and returns a list of Tweet objects

    Args:
        csv_file: A CSV file containing tweet data
    Returns:

        A list of Tweet objects
    """

    for row in csv_data:
        one_tweet = Tweet(
            int(row["tweet_id"]),
            int(row["user_id"]),
            row["tweet_ts"],
            row["tweet_text"],
        )
        api.post_tweet(one_tweet)


# Driver Code
if __name__ == "__main__":
    main(
        filename="hw1_data/tweets.csv"
    )  # set filename to tweets to initialize tweets table

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

"""
import time
import csv
import os
from your_database_module import your_insert_function

def track_insert_speed(csv_file):
    total_time = 0
    total_operations = 0

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row

        for row in reader:
            start_time = time.time()
            your_insert_function(row)  # Replace this with your actual function
            end_time = time.time()

            total_time += end_time - start_time
            total_operations += 1

    calls_per_second = total_operations / total_time if total_time > 0 else 0

    return calls_per_second

csv_file = os.path.join(os.path.dirname(__file__), 'your_file.csv')  # Replace with your actual CSV file path
print(f"API function calls per second: {track_insert_speed(csv_file)}")
"""
