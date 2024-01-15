-- creating user for this database
CREATE USER 'tweetuser'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON *.* TO 'tweetuser'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON Tweets.* TO 'tweetuser'@'localhost';
FLUSH PRIVILEGES;


-- create the database and tables for the tweet_py application

CREATE DATABASE IF NOT EXISTS TweetDB;

-- use the database
USE TweetDB;

-- create tweets table
DROP Tweets;
CREATE TABLE IF NOT EXISTS Tweets (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tweet_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet_text VARCHAR(140)
);

-- create follows table
--DROP Follows;
CREATE TABLE IF NOT EXISTS Follows (
    user_id INT,
    follows_id INT,
    PRIMARY KEY (user_id, follows_id)
);




