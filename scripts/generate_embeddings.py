import json
from sentence_transformers import SentenceTransformer
from scripts.chunk_documents import chunks

print("Loading embedding model: all-MiniLM-L6-v2")

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [chunk.page_content for chunk in chunks]

print(f"Generating embeddings for {len(texts)} chunks...")

embeddings = model.encode(
    texts,
    batch_size=32,
    show_progress_bar=True
)

records = []

for chunk, embedding in zip(chunks, embeddings):
    records.append({
        "content": chunk.page_content,
        "source": chunk.metadata.get("source"),
        "page_number": chunk.metadata.get("page"),
        "embedding": embedding.tolist()
    })

with open("output/embeddings.json", "w", encoding="utf-8") as f:
    json.dump(records, f)

print("Embeddings generated successfully.")
print(f"Number of embeddings: {len(records)}")
print(f"Embedding dimensions: {len(records[0]['embedding'])}")
print("Saved to output/embeddings.json")