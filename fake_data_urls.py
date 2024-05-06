import psycopg2
import random
import string

# Connect to PostgreSQL database
conn = psycopg2.connect("postgresql://hello_flask:hello_flask@localhost:1457")
cur = conn.cursor()

try:
    # Generate dummy data for URLs
    urls_data = []

    while True:  # Run indefinitely until the table reaches 1 million rows
        # Check the current length of the urls table
        cur.execute("SELECT COUNT(*) FROM urls")
        current_length = cur.fetchone()[0]
        
        if current_length >= 1000:  # If the length is 1 million or more, stop the loop
            break
        
        # Generate random URL
        url = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)) + ".com"  
        urls_data.append((url,))

        if len(urls_data) % 100 == 0:  # Insert rows in batches of 100
            cur.executemany("INSERT INTO urls (url) VALUES (%s)", urls_data)
            conn.commit()
            urls_data = []

except psycopg2.Error as e:
    print("Error:", e)

finally:
    # Close database connection
    cur.close()
    conn.close()
