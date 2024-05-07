import sys
import random
import psycopg2
from psycopg2 import errorcodes
from faker import Faker
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate fake data for testing.')
parser.add_argument('--urls', type=int, help='Number of rows for the urls table')
parser.add_argument('--users', type=int, help='Number of rows for the users table')
parser.add_argument('--tweets', type=int, help='Number of rows for the tweets table')
parser.add_argument('--db', type=str, help='Database connection string')
args = parser.parse_args()

# Connect to the PostgreSQL database
conn = psycopg2.connect(args.db)

# Create a cursor object
cur = conn.cursor()

# Faker instance for generating fake data
fake = Faker()

# Function to generate fake URLs and insert them into the urls table
def generate_urls(num_rows):
    for _ in range(num_rows):
        url = fake.url()
        try:
            cur.execute("INSERT INTO urls (url) VALUES (%s)", (url,))
        except psycopg2.IntegrityError as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                # Ignore unique constraint violation error
                pass
            else:
                print("Error inserting URL:", e)
            conn.rollback()
        else:
            conn.commit()

# Extract command line arguments
num_rows_urls = args.urls
num_rows_users = args.users
num_rows_tweets = args.tweets

# Generate fake data
generate_urls(num_rows_urls)

# Fill tables to reach the desired row counts
cur.execute("SELECT COUNT(*) FROM urls")
current_row_count = cur.fetchone()[0]
desired_row_count_urls = min(num_rows_urls + 10000, int(num_rows_urls * 1.1))  # 110% of the given row count
while current_row_count < num_rows_urls:
    additional_rows = min(desired_row_count_urls - current_row_count, num_rows_urls)
    generate_urls(additional_rows)
    cur.execute("SELECT COUNT(*) FROM urls")
    current_row_count = cur.fetchone()[0]

# Close cursor and connection
print("Insertion complete.")
cur.close()
conn.close()
