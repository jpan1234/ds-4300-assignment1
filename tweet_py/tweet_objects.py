

class Tweet:
    def __init__(self, user_id, tweet_text):
        self.user_id = user_id
        self.tweet_text = tweet_text

class Follows:
    def __init__(self, user_id, follows_id):
        self.user_id = user_id
        self.follows_id = follows_id

class User:
    def __init__(self, user_id):
        self.user_id = user_id