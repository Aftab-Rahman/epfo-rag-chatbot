from sentence_transformers import SentenceTransformer
import psycopg

# Load the same embedding model used for the documents
print("Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Ask the user for a question
query = input("\nEnter your question: ")

# Convert the question into an embedding
query_embedding = model.encode(query).tolist()

# Connect to PostgreSQL
conn = psycopg.connect(
    host="localhost",
    port=5433,
    dbname="chatbot_db",
    user="postgres",
    password="0001"
)

cursor = conn.cursor()

# Find the 5 most similar document chunks
cursor.execute(
    """
    SELECT content, source, page_number,
           embedding <=> %s::vector AS distance
    FROM documents
    ORDER BY embedding <=> %s::vector
    LIMIT 5;
    """,
    (query_embedding, query_embedding)
)

results = cursor.fetchall()

print("\nTop 5 relevant chunks:\n")

for i, (content, source, page_number, distance) in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(f"Source: {source}")
    print(f"Page: {page_number}")
    print(f"Distance: {distance:.4f}")
    print(f"Content:\n{content}\n")

cursor.close()
conn.close()

print("Search completed.")