FROM postgis/postgis:17-3.5

RUN apt-get update && apt-get install -y \
    less \
    make \
    vim \
    git \
    gcc \
    postgresql-server-dev-17

RUN pg_config --version \
 && test -f "$(pg_config --includedir-server)/postgres.h"

# install rum extensions from source
RUN cd /tmp \
 && pwd \
 && git clone https://github.com/postgrespro/rum \
 && pwd \
 && ls \
 && cd rum \
 && make USE_PGXS=1 \
 && make USE_PGXS=1 install \
 && rm -rf /tmp/rum

WORKDIR /tmp/db

RUN mkdir /data && chown postgres /data

# copy over the pagila database;
# we rename the files so that they get executed in the correct order
COPY schema.sql /docker-entrypoint-initdb.d/01.sql
