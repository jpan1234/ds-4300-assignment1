-- creating user for this database
CREATE USER 'tweetuser'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE, EXECUTE ON Tweets.* TO 'tweetuser'@'localhost';
FLUSH PRIVILEGES;


-- create the database and tables for the tweet_py application

CREATE DATABASE IF NOT EXISTS Tweets;

-- use the database
USE Tweets;

-- create tweets table
DROP TABLE Tweets;
CREATE TABLE IF NOT EXISTS Tweets (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tweet_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet_text VARCHAR(140)
);

-- create follows table
CREATE TABLE IF NOT EXISTS Follows (
    user_id INT,
    follows_id INT,
    PRIMARY KEY (user_id, follows_id)
);

CREATE INDEX t_user_id_index ON Tweets (user_id);

CREATE INDEX t_tweet_ts_index ON Tweets (tweet_ts);

CREATE INDEX f_follows_id_index ON Follows (follows_id);

CREATE INDEX f_user_id_index ON Follows (user_id);

-- create stored procedure to get timeline
DELIMITER $$
CREATE PROCEDURE get_timeline(IN check_user_id INT)
BEGIN
    SELECT DISTINCT F.follows_id, T.tweet_text, T.tweet_ts
    FROM Follows F
    INNER JOIN Tweets T on F.follows_id = T.user_id
    WHERE F.follows_id IN (SELECT follows_id FROM Follows WHERE user_id = check_user_id)
    AND F.user_id = check_user_id
    ORDER BY T.tweet_ts DESC
    LIMIT 10;
END $$
DELIMITER ;