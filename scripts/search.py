from sentence_transformers import SentenceTransformer
import psycopg
import ollama

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

# Build context from the retrieved chunks
context = ""

for i, (content, source, page_number, distance) in enumerate(results, start=1):
    print(f"--- Result {i} ---")
    print(f"Source: {source}")
    print(f"Page: {page_number}")
    print(f"Distance: {distance:.4f}")
    print(f"Content:\n{content}\n")

    context += f"""
[SOURCE {i}]
Source: {source}
Page: {page_number}
Content:
{content}

"""

cursor.close()
conn.close()

# Send the question and retrieved context to Ollama
print("Generating answer with Ollama...\n")

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "system",
            "content": (
                "You are a helpful RAG assistant. "
                "Answer the user's question using only the provided context. "
                "If the answer is not present in the context, say "
                "'I could not find the answer in the provided documents.' "
                "\n\n"
                "IMPORTANT CITATION RULES: "
                "Every factual statement based on the context must include "
                "the appropriate citation immediately after the statement, "
                "using [SOURCE 1], [SOURCE 2], etc. "
                "Do not add a separate 'According to' paragraph that repeats the answer. "
                "Do not invent or modify source numbers. "
                "Only cite sources that actually support the statement. "
                "If the context does not contain enough information, say so clearly."
            )
        },
        {
            "role": "user",
            "content": f"""
Question:
{query}

Context:
{context}

Answer the question based only on the context above.
Include the appropriate [SOURCE X] citation(s) for your answer.
"""
        }
    ]
)

# Display the final answer
print("\nFinal Answer:")
print(response["message"]["content"])

print("\nSearch completed.")