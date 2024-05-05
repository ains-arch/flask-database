#!/bin/bash

files=$(find data/*)

source .env.prod

echo 'load pg_normalized'
echo "$files" | parallel python3 load_tweets.py --db=postgresql://$PGUSER:$PGPASSWORD@localhost:1467 --inputs "$file"
