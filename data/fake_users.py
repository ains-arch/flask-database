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

# Function to generate fake users and insert them into the users table
def generate_users(num_rows, num_urls):
    for i in range(num_rows):
        name = fake.user_name()
        password = fake.password()
        id_urls = random.randint(1, num_urls)
        try:
            cur.execute("INSERT INTO users (name, password, id_urls) VALUES (%s, %s, %s)", (name, password, id_urls))
        except psycopg2.IntegrityError as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                # Ignore unique constraint violation error
                pass
            elif e.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
                # Ignore foreign key violation error
                pass
            else:
                print("Error inserting user:", e)
            conn.rollback()
        else:
            conn.commit()

# Extract command line arguments
num_rows_urls = args.urls
num_rows_users = args.users
num_rows_tweets = args.tweets

# Generate fake data
generate_users(num_rows_users, num_rows_urls)

# Fill tables to reach the desired row counts
cur.execute("SELECT COUNT(*) FROM users")
current_row_count = cur.fetchone()[0]
desired_row_count_users = min(num_rows_users+10000, int(num_rows_users * 1.1))  # 110% of the given row count
while current_row_count < num_rows_users:
    additional_rows = min(desired_row_count_users - current_row_count, num_rows_users)
    generate_users(additional_rows, num_rows_urls)  # Assuming num_rows_urls is the total number of URLs
    cur.execute("SELECT COUNT(*) FROM users")
    current_row_count = cur.fetchone()[0]

# Close cursor and connection
print("Insertion complete.")
cur.close()
conn.close()
