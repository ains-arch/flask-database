import psycopg2
import random
from faker import Faker
from datetime import datetime, timedelta

# Connect to PostgreSQL database
conn = psycopg2.connect("postgresql://hello_flask:hello_flask@localhost:1457")
cur = conn.cursor()

fake = Faker()

try:
    # Generate dummy data for Tweets
    tweets_data = []

    for id_tweets in range(1, 501):  # Iterate over id_tweets from 1 to 500
        id_users = random.randint(1, 500)  # Choose a random user ID between 1 and 500
        id_urls = random.randint(501, 1000)  # Choose a random URL ID between 501 and 1000
        created_at = fake.date_time_between(start_date="-1y", end_date="now", tzinfo=None)  # Generate random date within the last year
        text = fake.text()  # Generate random tweet text
        
        tweets_data.append((id_tweets, id_users, id_urls, created_at, text))

    # Insert Tweets data into database
    cur.executemany("INSERT INTO tweets (id_tweets, id_users, id_urls, created_at, text) VALUES (%s, %s, %s, %s, %s)", tweets_data)
    conn.commit()

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Close database connection
    cur.close()
    conn.close()
