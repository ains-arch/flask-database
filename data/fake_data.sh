#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <num_urls> <num_users> <num_tweets> <environment>"
    exit 1
fi

# Assign arguments to variables
num_urls=$1
num_users=$2
num_tweets=$3
environment=$4

# Determine the connection string based on the environment
if [ "$environment" = "dev" ]; then
    db_connection_string="postgresql://hello_flask:hello_flask@localhost:1457"
elif [ "$environment" = "prod" ]; then
    source .env.prod
    db_connection_string="postgresql://$PGUSER:$PGPASSWORD@localhost:1467"
else
    echo "Invalid environment specified. Please specify 'dev' or 'prod'."
    exit 1
fi

# Run fake_urls.py script
echo "Generating URLs..."
time python3 fake_urls.py --urls=$num_urls  --db="$db_connection_string"
echo "Inserted URLs."

# Run fake_users.py script
echo "Generating users..."
time python3 fake_users.py --urls=$num_urls --users=$num_users --db="$db_connection_string"
echo "Inserted users."

# Run fake_tweets.py script
echo "Generating tweets..."
time python3 fake_tweets.py --urls=$num_urls --users=$num_users --tweets=$num_tweets --db="$db_connection_string"
echo "Inserted tweets."
