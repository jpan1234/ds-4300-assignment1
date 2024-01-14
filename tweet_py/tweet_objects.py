

class Tweet:

    def __init__(self, user, content, timestamp):
        self.user = user
        self.content = content
        self.timestamp = timestamp

class User:

    def __init__(self, username, followers, following, bio):
        self.username = username
        self.followers = followers
        self.following = following
        self.bio = bio

    def __str__(self):
        return f"User: {self.username}, Followers: {self.followers}, Following: {self.following}"