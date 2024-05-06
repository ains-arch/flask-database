#!/bin/bash

# Check if correct number of arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <num_users> <num_tweets> <num_urls>"
    exit 1
fi

# Run the Python script with provided arguments
python3 fake_data.py "$1" "$2" "$3"
