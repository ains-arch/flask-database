# flask-on-docker
[![tests](https://github.com/ains-arch/flask-database/actions/workflows/tests_dev.yml/badge.svg)](https://github.com/ains-arch/flask-database/actions/workflows/tests_dev.yml)

## Overview

This repo contains all the necessary files to host a simple web app.
The development environment configures the default Flask development server
to run on Docker with Postgres.
The production environmental also includes Nginx and Gunicorn,
and supports serving both static and user-uploaded media files via Nginx. 

## Build Instructions

### Development

Build the images and run the containers:

```sh
docker-compose up -d --build
```

Check it worked as expected:

```sh
docker-compose logs
```

Test it out at [http://localhost:8080](http://localhost:8080).

Add the data:

This may take up to a few minutes, depending on the load on the server.

```sh
./load_tweets_dev.sh
```

Check the data loaded correctly:

```sh
docker-compose exec -T db ./run_tests.sh
```

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
./load_tweets_prod.sh
```

Check that the data loaded correctly:

```sh
source .env.prod
docker-compose exec -e PGUSER="$PGUSER" -e PGPASSWORD="$PGPASSWORD" -T db ./run_tests.sh
```
