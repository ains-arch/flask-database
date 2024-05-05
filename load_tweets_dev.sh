#!/bin/sh

files=$(find data/*)

echo 'load pg_normalized'
echo "$files" | parallel python3 load_tweets.py --db=postgresql://hello_flask:hello_flask@localhost:1457 --inputs "$file"
