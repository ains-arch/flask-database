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

# Function to generate fake tweets and insert them into the tweets table
def generate_tweets(num_rows, num_users, num_urls):
    tweets = []
    for _ in range(num_rows):
        id_users = random.randint(1, num_users)
        id_urls = random.randint(1, num_urls)
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        text = fake.text(max_nb_chars=140)
        tweets.append((id_users, id_urls, created_at, text))
    return tweets

def generate_tweets_batch(num_rows, num_users, num_urls):
    tweets = generate_tweets(num_rows, num_users, num_urls)
    try:
        cur.executemany("INSERT INTO tweets (id_users, id_urls, created_at, text) VALUES (%s, %s, %s, %s)",
                        [tuple(tweet) for tweet in tweets])
        conn.commit()
    except psycopg2.IntegrityError as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            # Ignore unique constraint violation error
            pass
        elif e.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
            pass
        else:
            print("Error inserting tweet:", e)
        conn.rollback()

# Extract command line arguments
num_rows_urls = args.urls
num_rows_users = args.users
num_rows_tweets = args.tweets

batch_size = 1000

# Fill tables to reach the desired row counts
cur.execute("SELECT COUNT(*) FROM tweets")
current_row_count = cur.fetchone()[0]
missing_rows = num_rows_tweets - current_row_count
while current_row_count < num_rows_tweets:
    generate_tweets_batch(batch_size, num_rows_users, num_rows_urls)
    cur.execute("SELECT COUNT(*) FROM tweets")
    current_row_count = cur.fetchone()[0]

# Close cursor and connection
print("Insertion complete.")
cur.close()
conn.close()
