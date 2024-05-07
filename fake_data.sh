#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <num_rows_urls> <num_rows_users> <num_rows_tweets>"
    exit 1
fi

# Assign arguments to variables
num_rows_urls=$1
num_rows_users=$2
num_rows_tweets=$3

# Run fake_data.py script with arguments in parallel
time python3 fake_data.py $num_rows_urls $num_rows_users $num_rows_tweets &
