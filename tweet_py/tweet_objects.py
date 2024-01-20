class Tweet:
    def __init__(self, user_id, tweet_text, tweet_ts):
        self.user_id = user_id
        self.tweet_text = tweet_text
        self.tweet_ts = tweet_ts


class Follows:
    def __init__(self, user_id, follows_id):
        self.user_id = user_id
        self.follows_id = follows_id


class User:
    def __init__(self, user_id):
        self.user_id = user_id
