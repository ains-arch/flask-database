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
parser.add_argument('--db', type=str, help='Database connection string')
args = parser.parse_args()

# Connect to the PostgreSQL database
conn = psycopg2.connect(args.db)

# Create a cursor object
cur = conn.cursor()

# Faker instance for generating fake data
fake = Faker()

# Function to generate fake users and insert them into the users table in batches
def generate_users(num_rows, num_urls):
    users = []
    for _ in range(num_rows):
        name = fake.user_name() + ''.join([str(random.randint(0, 9)) for _ in range(8)])
        password = fake.password()
        id_urls = random.randint(1, num_urls)
        users.append((name, password, id_urls))
    return users

# Function to generate fake users and insert them into the users table in batches
def generate_users_batch(users):
    try:
        cur.executemany("INSERT INTO users (name, password, id_urls) VALUES (%s, %s, %s)", users)
        conn.commit()
    except psycopg2.Error as e:
        print("Error inserting users:", e)
        conn.rollback()

# Extract command line arguments
num_rows_urls = args.urls
num_rows_users = args.users

# Generate fake data in batches
batch_size = 100
while num_rows_users > 0:
    batch_rows = min(num_rows_users, batch_size)
    users = generate_users(batch_rows, num_rows_urls)
    generate_users_batch(users)
    num_rows_users -= batch_rows

# Close cursor and connection
print("Insertion complete.")
cur.close()
conn.close()
