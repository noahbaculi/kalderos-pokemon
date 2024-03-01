import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="myuser",
    user="myuser",
    password="mypassword",
    host="localhost",
    port="5432",
)

# Create a cursor
cur = conn.cursor()

# Execute SQL queries
cur.execute("SELECT * FROM pokemon;")
print(f"{cur.statusmessage = }")
rows = cur.fetchall()
for row in rows:
    print(row)

# Close the cursor and connection
cur.close()
conn.close()
