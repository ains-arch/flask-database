\set ON_ERROR_STOP on

BEGIN;

CREATE TABLE urls (
    id_urls BIGSERIAL PRIMARY KEY,
    url TEXT UNIQUE
);

/*
 * Users may be partially hydrated with only a name/screen_name 
 * if they are first encountered during a quote/reply/mention 
 * inside of a tweet someone else's tweet.
 */
CREATE TABLE users (
    id_users BIGINT PRIMARY KEY,
    id_urls BIGINT REFERENCES urls(id_urls),
    name TEXT,
    FOREIGN KEY (id_urls) REFERENCES urls(id_urls)
);

/*
 * Tweets may be entered in hydrated or unhydrated form.
 */
CREATE TABLE tweets (
    id_tweets BIGINT PRIMARY KEY,
    id_users BIGINT,
    in_reply_to_status_id BIGINT,
    in_reply_to_user_id BIGINT,
    quoted_status_id BIGINT,
    text TEXT,
    FOREIGN KEY (id_users) REFERENCES users(id_users),
    FOREIGN KEY (in_reply_to_user_id) REFERENCES users(id_users)

    -- NOTE:
    -- We do not have the following foreign keys because they would require us
    -- to store many unhydrated tweets in this table.
    -- FOREIGN KEY (in_reply_to_status_id) REFERENCES tweets(id_tweets),
    -- FOREIGN KEY (quoted_status_id) REFERENCES tweets(id_tweets)
);

CREATE TABLE tweet_urls (
    id_tweets BIGINT,
    id_urls BIGINT,
    PRIMARY KEY (id_tweets, id_urls),
    FOREIGN KEY (id_tweets) REFERENCES tweets(id_tweets),
    FOREIGN KEY (id_urls) REFERENCES urls(id_urls)
);

COMMIT;
