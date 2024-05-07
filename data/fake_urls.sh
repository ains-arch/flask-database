#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 <num_rows_urls> <num_rows_users> <num_rows_tweets> <environment>"
    echo "Environment options: dev, prod"
    exit 1
fi

# Assign arguments to variables
num_rows_urls=$1
num_rows_users=$2
num_rows_tweets=$3
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

# Run fake_data.py script with arguments in parallel
time python3 fake_urls.py --urls=$num_rows_urls --users=$num_rows_users --tweets=$num_rows_tweets --db="$db_connection_string"

