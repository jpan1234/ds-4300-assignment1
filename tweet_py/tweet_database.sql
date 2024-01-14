-- create the database and tables for the tweet_py application
CREATE DATABASE IF NOT EXISTS Tweets;

-- use the database
USE Tweets;

-- 
CREATE TABLE IF NOT EXISTS TWEET (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tweet_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet_text VARCHAR(140)
);

CREATE TABLE IF NOT EXISTS FOLLOWS (
    user_id INT,
    follows_id INT,
    PRIMARY KEY (user_id, follows_id)
);