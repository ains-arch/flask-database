import psycopg2
import random
import string

# Connect to PostgreSQL database
conn = psycopg2.connect("postgresql://hello_flask:hello_flask@localhost:1457")
cur = conn.cursor()

try:
    # Generate dummy data for Users
    users_data = []

    for id_urls in range(1, 501):  # Iterate over the first 500 id_urls
        # Generate unique name and password
        name = ''.join(random.choices(string.ascii_lowercase, k=8))  # Generate random name
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))  # Generate random password
        
        users_data.append((name, password, id_urls))

    # Insert Users data into database
    cur.executemany("INSERT INTO users (name, password, id_urls) VALUES (%s, %s, %s)", users_data)
    conn.commit()

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Close database connection
    cur.close()
    conn.close()
