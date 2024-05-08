# flask-on-docker
[![tests](https://github.com/ains-arch/flask-database/actions/workflows/tests_dev.yml/badge.svg)](https://github.com/ains-arch/flask-database/actions/workflows/tests_dev.yml)

## Overview

This repo contains all the necessary files to host a simple web app.
The development environment configures the default Flask development server
to run on Docker with Postgres.
The production environmental also includes Nginx and Gunicorn,
and supports serving both static and user-uploaded media files via Nginx. 

## Build Instructions

First, if you're able, remove the volumes you've created in previous work
to free up disk space.

```sh
$ docker stop $(docker ps -q)
$ docker rm $(docker ps -qa)
$ docker volume prune --all
```

### Development

Build the images and run the containers:

```sh
$ docker-compose up -d --build
```

Check it worked as expected:

```sh
$ docker-compose -f docker-compose.yml logs dbd
$ docker-compose -f docker-compose.yml logs webd
```

Test it out at [http://localhost:1361](http://localhost:1361).

Add a small amount of data:

Note that this may take a few minutes depending on the load on your server.

```sh
$ cd data
$ ./fake_data.sh 10000 1000 1000 dev
Generating URLs...
Insertion complete.
...
Inserted URLs.
Generating users...
Insertion complete.
...
Inserted users.
Generating tweets...
Insertion complete.
...
Inserted tweets.
$ cd ..
```

Check the data loaded correctly:

```sh
$ docker-compose exec dbd psql
psql (16.2 (Debian 16.2-1.pgdg110+2))
Type "help" for help.
hello_flask=#
```
```sql
SELECT
    'urls' AS table_name,
    COUNT(*) AS row_count
FROM
    urls
UNION ALL
SELECT
    'users' AS table_name,
    COUNT(*) AS row_count
FROM
    users
UNION ALL
SELECT
    'tweets' AS table_name,
    COUNT(*) AS row_count
FROM
    tweets;
 table_name | row_count
------------+-----------
 urls       |     10000
 users      |      1000
 tweets     |      1000
(3 rows)
```

### Production

Create a `.env.prod` file in the root folder of the project. Choose a username and password.

```sh
FLASK_APP=project/__init__.py
FLASK_DEBUG=0
DATABASE_URL=postgresql://$YOUR USERNAME HERE:$YOUR PASSWORD HERE@db:5432
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
APP_FOLDER=/home/app/web
PGUSER=$YOUR USERNAME HERE
PGPASSWORD=$YOUR PASSWORD HERE
```

Create a `.env.prod.db` file in the root folder of the project. Use the same username and password.

```sh
POSTGRES_USER=$YOUR USERNAME HERE
POSTGRES_PASSWORD=$YOUR PASSWORD HERE
```

Copy the `.env.prod` file into the data folder.

```sh
$ cp .env.prod data
```

Edit the `services/web/project/__init__.py` file to include your database credentials.

Build the images and run the containers:

```sh
$ docker-compose -f docker-compose.prod.yml up -d --build
```

Test it out at [http://localhost:1447](http://localhost:1447)!

Add the data:

```sh
$ cd data
$ nohup ./fake_data.sh 10000000 1000000 1000000 prod > data_load_prod.log &
$ cat data_tweets.log
nohup: ignoring input
Generating URLs...
Insertion complete.

real    56m25.733s
user    25m13.258s
sys     3m17.477s
Inserted URLs.
Generating users...
Insertion complete.

real    8m50.155s
user    4m15.048s
sys     0m16.419s
Inserted users.
Generating tweets...
Insertion complete.

real    8m14.107s
user    2m29.554s
sys     0m21.445s
Inserted tweets.
$ cd ..
```

In order to speed up data insertion, it may be helpful to drop
and recreate the indexes.

```sh
$ source .env.prod
$ docker-compose -f docker-compose.prod.yml exec -e PGUSER="$PGUSER" -e PGPASSWORD="$PGPASSWORD" db psql
psql (16.2 (Debian 16.2-1.pgdg110+2))
Type "help" for help.
$YOUR USERNAME HERE=#
```
```sql
DROP INDEX users_id_urls_idx,
           users_name_idx,
           tweets_id_users_idx,
           tweets_created_at_idx,
           tweets_id_url_idx,
           tweets_text_rum_idx,
           tweets_created_at_id_tweets_idx;
```

Make sure you recreate them once the load is complete.
```sql
CREATE INDEX users_id_urls_idx ON users (id_urls);
CREATE INDEX users_name_idx ON users(name);
CREATE INDEX tweets_id_users_idx ON tweets (id_users);
CREATE INDEX tweets_created_at_idx ON tweets (created_at);
CREATE INDEX tweets_id_url_idx ON tweets (id_urls);
CREATE INDEX tweets_text_rum_idx ON tweets USING rum (to_tsvector('english', text) rum_tsvector_ops);
CREATE INDEX tweets_created_at_id_tweets_idx ON tweets(created_at DESC, id_tweets);
```

Log into the database to check that the data loaded correctly:

```sql
SELECT
    'urls' AS table_name,
    COUNT(*) AS row_count
FROM
    urls
UNION ALL
SELECT
    'users' AS table_name,
    COUNT(*) AS row_count
FROM
    users
UNION ALL
SELECT
    'tweets' AS table_name,
    COUNT(*) AS row_count
FROM
    tweets;
 table_name | row_count
------------+-----------
 urls       |  10000000
 users      |   1000000
 tweets     |   1000000
(3 rows)
```

Your website should now be up and running!
