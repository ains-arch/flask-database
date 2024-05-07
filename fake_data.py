import sys
import random
import psycopg2
from psycopg2 import errorcodes
from faker import Faker

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    dbname="hello_flask",
    user="hello_flask",
    password="hello_flask",
    host="localhost",
    port="1457"
)

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

# Function to generate fake tweets and insert them into the tweets table
def generate_tweets(num_rows, num_users, num_urls):
    for i in range(num_rows):
        id_users = random.randint(1, num_users)
        id_urls = random.randint(1, num_urls)
        created_at = fake.date_time_between(start_date='-1y', end_date='now')
        text = fake.text()
        try:
            cur.execute("INSERT INTO tweets (id_users, id_urls, created_at, text) VALUES (%s, %s, %s, %s)",
                        (id_users, id_urls, created_at, text))
        except psycopg2.IntegrityError as e:
            if e.pgcode == errorcodes.UNIQUE_VIOLATION:
                # Ignore unique constraint violation error
                pass
            elif e.pgcode == errorcodes.FOREIGN_KEY_VIOLATION:
                pass
            else:
                print("Error inserting tweet:", e)
            conn.rollback()
        else:
            conn.commit()

# Extract command line arguments
num_rows_urls = int(sys.argv[1])
num_rows_users = int(sys.argv[2])
num_rows_tweets = int(sys.argv[3])

# Calculate half of the max IDs for users and tweets
half_ids = max(num_rows_urls, num_rows_users) // 2

# Generate fake data
generate_urls(num_rows_urls)
generate_users(num_rows_users, num_rows_urls)
generate_tweets(num_rows_tweets, num_rows_users, num_rows_urls)

# Fill tables to reach the desired row counts
cur.execute("SELECT COUNT(*) FROM urls")
current_row_count = cur.fetchone()[0]
desired_row_count_urls = int(num_rows_urls * 1.1)  # 110% of the given row count
while current_row_count < num_rows_urls:
    additional_rows = min(desired_row_count_urls - current_row_count, num_rows_urls)
    generate_urls(additional_rows)
    cur.execute("SELECT COUNT(*) FROM urls")
    current_row_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM users")
current_row_count = cur.fetchone()[0]
desired_row_count_users = int(num_rows_users * 1.1)  # 110% of the given row count
while current_row_count < num_rows_users:
    additional_rows = min(desired_row_count_users - current_row_count, num_rows_users)
    generate_users(additional_rows, num_rows_urls)  # Assuming num_rows_urls is the total number of URLs
    cur.execute("SELECT COUNT(*) FROM users")
    current_row_count = cur.fetchone()[0]

cur.execute("SELECT COUNT(*) FROM tweets")
current_row_count = cur.fetchone()[0]
desired_row_count_tweets = int(num_rows_tweets * 1.1)  # 110% of the given row count
while current_row_count < num_rows_tweets:
    additional_rows = min(desired_row_count_tweets - current_row_count, num_rows_tweets)
    generate_tweets(additional_rows, num_rows_users, num_rows_urls)
    cur.execute("SELECT COUNT(*) FROM tweets")
    current_row_count = cur.fetchone()[0]

# Close cursor and connection
print("Insertion complete.")
cur.close()
conn.close()
