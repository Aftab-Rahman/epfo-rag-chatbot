import psycopg

conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="postgres",
    user="postgres",
    password="0001"
)

print("✅ PostgreSQL connection successful!")

with conn.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM epfo_chunks;")
    count = cur.fetchone()[0]
    print(f"epfo_chunks currently contains {count} rows.")

conn.close()
print("Connection closed.")