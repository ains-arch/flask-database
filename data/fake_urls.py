import sys
import random
import psycopg2
from psycopg2 import errorcodes
from faker import Faker
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description='Generate fake data for testing.')
parser.add_argument('--urls', type=int, help='Number of rows for the urls table')
parser.add_argument('--db', type=str, help='Database connection string')
args = parser.parse_args()

# Connect to the PostgreSQL database
conn = psycopg2.connect(args.db)

# Create a cursor object
cur = conn.cursor()

# Faker instance for generating fake data
fake = Faker()

# Function to generate fake URLs and insert them into the urls table in batches
def generate_urls_batch(num_rows):
    urls = [(fake.url(),) for _ in range(num_rows)]
    try:
        cur.executemany("INSERT INTO urls (url) VALUES (%s)", urls)
        conn.commit()
    except psycopg2.IntegrityError as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            # Ignore unique constraint violation error
            print("oops")
        else:
            print("Error inserting URL:", e)
        conn.rollback()

# Extract command line arguments
num_rows_urls = args.urls

# Generate fake data in batches
batch_size = 10000

# Fill tables to reach the desired row counts
cur.execute("SELECT COUNT(*) FROM urls")
current_row_count = cur.fetchone()[0]
missing_rows = num_rows_urls - current_row_count
while current_row_count < num_rows_urls:
    generate_urls_batch(batch_size)
    cur.execute("SELECT COUNT(*) FROM urls")
    current_row_count = cur.fetchone()[0]

# Close cursor and connection
print("Insertion complete.")
cur.close()
conn.close()
