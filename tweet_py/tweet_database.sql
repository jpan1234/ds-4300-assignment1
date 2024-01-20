-- creating user for this database
CREATE USER 'tweetuser'@'localhost' IDENTIFIED BY 'password';
GRANT SELECT, INSERT, UPDATE, DELETE ON Tweets.* TO 'tweetuser'@'localhost';
FLUSH PRIVILEGES;


-- create the database and tables for the tweet_py application

CREATE DATABASE IF NOT EXISTS Tweets;

-- use the database
USE Tweets;

-- create tweets table
TRUNCATE TABLE Tweets.Tweets;
CREATE TABLE IF NOT EXISTS Tweets (
    tweet_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    tweet_ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    tweet_text VARCHAR(140)
);

-- create follows table
--DROP TABLE Follows;
CREATE TABLE IF NOT EXISTS Follows (
    user_id INT,
    follows_id INT,
    PRIMARY KEY (user_id, follows_id)
);

CREATE INDEX t_user_id_index ON Tweets (user_id);

CREATE INDEX t_tweet_ts_index ON Tweets (tweet_ts);

CREATE INDEX f_follows_id_index ON Follows (follows_id);

CREATE INDEX f_user_id_index ON Follows (user_id);

SELECT T.tweet_id, T.user_id, T.tweet_ts, T.tweet_text
            FROM Tweets T
            INNER JOIN Follows F ON T.user_id = F.follows_id
            WHERE T.user_id = 1
            ORDER BY T.tweet_ts DESC
            LIMIT 10;

CREATE PROCEDURE get_timeline(IN user_id INT);
BEGIN
    SELECT T.tweet_id, T.user_id, T.tweet_ts, T.tweet_text
    FROM Tweets T
    INNER JOIN Follows F ON T.user_id = F.follows_id
    WHERE T.user_id = user_id
    ORDER BY T.tweet_ts DESC
    LIMIT 10;
END;
        FROM Tweets T
        LEFT JOIN Follows F ON T.user_id = F.follows_id
        WHERE T.user_id = 3
        ORDER BY T.tweet_ts DESC
        LIMIT 10;


SELECT * FROM Follows WHERE user_id = 2281;

SELECT * FROM Tweets WHERE user_id = 2281;

SELECT DISTINCT T.user_id, F.follows_id
FROM Tweets T
INNER JOIN Follows F on T.user_id = F.user_id
WHERE T.user_id = 2281;


SELECT * FROM Follows;

SELECT DISTINCT T.tweet_text, F.follows_id, T.tweet_ts
FROM Follows F
INNER JOIN Tweets T on F.follows_id = T.user_id
WHERE F.follows_id IN (SELECT follows_id FROM Follows WHERE user_id = 2281)
AND F.user_id = 2281
LIMIT 10;
