import json
import psycopg

# PostgreSQL connection
conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="chatbot_db",
    user="postgres",
    password="0001"
)

cursor = conn.cursor()

# load chunks are replaced with load embeddings as chunks are already loaded in generate_embeddings.py 
# and stored in embeddings.json

# Load chunks
# with open("output/chunks.txt", "r", encoding="utf-8") as f:
#    content = f.read()

# Load embeddings
with open("output/embeddings.json", "r", encoding="utf-8") as f:
    records = json.load(f)

print(f"Loaded {len(records)} records.")
print("Connected to PostgreSQL.")
#print("Ready to store embeddings.")

for record in records:
    cursor.execute(
        """
        INSERT INTO documents (content, source, page_number, embedding)
        VALUES (%s, %s, %s, %s)
        """,
        (
            record["content"],
            record["source"],
            record["page_number"],
            record["embedding"]
        )
    )

conn.commit()

print(f"Stored {len(records)} records in PostgreSQL.")

cursor.close()
conn.close()

print("Connection closed.")