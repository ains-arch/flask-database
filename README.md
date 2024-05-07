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
$ docker-compose logs
```

Test it out at [http://localhost:8080](http://localhost:8080).

Add a small amount of data:

Note that this may take a few minutes depending on the load on your server.

```sh
$ ./fake_data.sh 10000 1000 1000 dev
Insertion complete.

real    0m20.361s
user    0m7.521s
sys     0m1.130s
```

Check the data loaded correctly:

```sh
$ docker-compose exec db psql
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
 urls       |     10387
 users      |      1009
 tweets     |      1049
(3 rows)
```

Due to randomness in the data generation, your numbers will be a little
different than mine. They should all be equal to or greater than the input
row numbers, though.

### Production

1. Create a *.env.prod* file in the root folder of the project. Choose a username and password.

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

2. Create a *.env.prod.db* file in the root folder of the project. Use the same username and password.

```sh
POSTGRES_USER=$YOUR USERNAME HERE
POSTGRES_PASSWORD=$YOUR PASSWORD HERE
```

3. Build the images and run the containers:

```sh
docker-compose -f docker-compose.prod.yml up -d --build
```

Test it out at [http://localhost:8181](http://localhost:8181)!

Add the data:

```sh
./fake_data.sh 10000 1000 1000 prod
Insertion complete.

real    0m21.465s
user    0m7.645s
sys     0m1.431s
```

Check that the data loaded correctly:

```sh
source .env.prod
docker-compose exec -e PGUSER="$PGUSER" -e PGPASSWORD="$PGPASSWORD" db psql
psql (16.2 (Debian 16.2-1.pgdg110+2))
Type "help" for help.
$YOUR USERNAME HERE=#
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
 urls       |     10403
 users      |      1010
 tweets     |      1056
(3 rows)
```
