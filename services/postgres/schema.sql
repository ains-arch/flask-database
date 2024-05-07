\set ON_ERROR_STOP on

BEGIN;

CREATE EXTENSION rum;
    
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
    id_users BIGSERIAL PRIMARY KEY,
    name TEXT UNIQUE,
    password TEXT,
    id_urls BIGINT,
    FOREIGN KEY (id_urls) REFERENCES urls(id_urls)
);

/*
 * Since the id_urls column in the users table is a foreign key
 * referencing the urls table, creating an index on it can speed
 * up queries that involve joining or filtering based on this column.
 */
CREATE INDEX users_id_urls_idx ON users (id_urls);

CREATE INDEX users_name_idx ON users(name);

/*
 * Tweets may be entered in hydrated or unhydrated form.
 */
CREATE TABLE tweets (
    id_tweets BIGSERIAL PRIMARY KEY,
    id_users BIGINT,
    id_urls BIGINT,
    created_at TIMESTAMPTZ,
    text TEXT,
    FOREIGN KEY (id_users) REFERENCES users(id_users),
    FOREIGN KEY (id_urls) REFERENCES urls(id_urls)
);

/*
 * If you frequently query tweets based on the user they belong to,
 * creating an index on the id_users column in the tweets table
 * can improve query performance.
 */
CREATE INDEX tweets_id_users_idx ON tweets (id_users);

/*
 * If you frequently search for tweets based on the created_at timestamp, 
 * add an index on that column.
 */

CREATE INDEX tweets_created_at_idx ON tweets (created_at);

/*
 * If you frequently query tweets based on the url they have,
 * create an index on the id_urls column in the tweets table
 * can improve query performance.
 */
CREATE INDEX tweets_id_url_idx ON tweets (id_urls);

/*
 * RUM index, when I have it installed
*/
CREATE INDEX tweets_text_rum_idx ON tweets USING rum (to_tsvector('english', text) rum_tsvector_ops);

CREATE INDEX tweets_created_at_id_tweets_idx ON tweets(created_at DESC, id_tweets);

COMMIT;
