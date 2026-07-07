# RAG Chatbot — Provident Fund (EPFO)

A Retrieval-Augmented Generation (RAG) chatbot built to answer questions about India's Provident Fund, using data sourced from the official EPFO website. Designed with guardrails to prevent hallucination and ensure safe, grounded responses.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| LLM & Embeddings | Ollama (local) |
| Vector Store | PostgreSQL + pgvector |
| IDE | VS Code |
| Data Source | EPFO Official Website (PDF) |

---

## Project Goal

Build a chatbot that:
- Answers user questions strictly based on EPFO/PF official data
- Does **not** hallucinate or go beyond the provided knowledge base
- Uses guardrails to ensure safe, accurate, and grounded responses

---

## Pipeline Overview

```
PDF → Extract Text → Chunk → Embed → Store in pgvector → Retrieve → LLM → Answer
```

---

## Step-by-Step Implementation

### Step 1 — Extract Text from PDF

Using **PyMuPDF** to extract text page by page, preserving page numbers for citation.

```python
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for page_num, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page": page_num + 1,
            "text": text
        })
    return pages
```

**Install:** `pip install pymupdf`

> Page numbers are stored so the chatbot can cite which page an answer came from.

---

### Step 2 — Chunking

Splits extracted text into smaller, overlapping pieces for better search precision.

```python
def chunk_text(pages, chunk_size=500, overlap=100):
    chunks = []

    for page_data in pages:
        text = page_data["text"]
        words = text.split()

        start = 0
        while start < len(words):
            end = start + chunk_size
            chunk_words = words[start:end]
            chunk_text = " ".join(chunk_words)

            chunks.append({
                "text": chunk_text,
                "page": page_data["page"],
                "chunk_index": len(chunks)
            })

            # Overlap ensures answers spanning chunk boundaries aren't lost
            start += chunk_size - overlap

    return chunks
```

**Why overlap?** If an answer spans two chunks, the 100-word overlap ensures it isn't cut off at the boundary.

---

### Step 3 — Embedding

Converts each chunk into a vector (list of numbers) that captures its meaning. Similar meaning = similar vectors.

```python
import ollama

def embed_chunks(chunks):
    embedded = []

    for chunk in chunks:
        response = ollama.embeddings(
            model="nomic-embed-text",
            prompt=chunk["text"]
        )

        embedded.append({
            **chunk,
            "embedding": response["embedding"]  # ~768 floats
        })

    return embedded
```

**Pull the model first:** `ollama pull nomic-embed-text`

> `nomic-embed-text` runs fully locally via Ollama and produces 768-dimensional vectors — no API key or internet needed.

---

### Step 4 — Store in PostgreSQL + pgvector

#### Database Setup (run once)

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE epfo_chunks (
    id          SERIAL PRIMARY KEY,
    text        TEXT NOT NULL,
    page        INTEGER,
    chunk_index INTEGER,
    embedding   vector(768)
);
```

#### Python — Insert Chunks

```python
import psycopg2
import json

conn = psycopg2.connect(
    dbname="your_db",
    user="your_user",
    password="your_password",
    host="localhost"
)
cur = conn.cursor()

def store_chunks(embedded_chunks):
    for chunk in embedded_chunks:
        cur.execute("""
            INSERT INTO epfo_chunks (text, page, chunk_index, embedding)
            VALUES (%s, %s, %s, %s)
        """, (
            chunk["text"],
            chunk["page"],
            chunk["chunk_index"],
            json.dumps(chunk["embedding"])
        ))

    conn.commit()
    print(f"Stored {len(embedded_chunks)} chunks.")
```

**Install:** `pip install psycopg2-binary`

---

### Step 5 — Run the Full Pipeline

```python
# main.py
pdf_path = "epfo_provident_fund.pdf"

print("Extracting text...")
pages = extract_text_from_pdf(pdf_path)

print("Chunking...")
chunks = chunk_text(pages, chunk_size=500, overlap=100)
print(f"  → {len(chunks)} chunks created")

print("Embedding...")
embedded = embed_chunks(chunks)

print("Storing in pgvector...")
store_chunks(embedded)

print("Done! Knowledge base is ready.")
```

---

## What the Database Looks Like After This

```
epfo_chunks table
──────────────────────────────────────────────────────────────
 id │ text                            │ page │ embedding
  1 │ "EPF contribution is 12% of..." │  3   │ [0.12, -0.45, ...]
  2 │ "Withdrawal rules state that..."│  3   │ [0.08, -0.31, ...]
```

When a user asks *"What is the PF withdrawal rule?"*, the question is embedded the same way, and the closest matching chunks are retrieved — that's the **retrieval** step.

---

## Checklist — Before Moving to Retrieval

- [ ] `ollama pull nomic-embed-text` done
- [ ] pgvector extension enabled in PostgreSQL
- [ ] PDF extracted — print a few chunks to verify quality
- [ ] `epfo_chunks` table created with `vector(768)` column
- [ ] Full pipeline runs end to end

---

## Coming Next

- [ ] Retrieval — semantic search with pgvector
- [ ] LLM call — passing retrieved chunks as context to Ollama
- [ ] Guardrails — preventing hallucination, keeping answers grounded in EPFO data only
- [ ] Chat interface — building the actual question-answer loop

---

## Project Structure (Planned)

```
rag-chatbot-epfo/
├── data/
│   └── epfo_provident_fund.pdf
├── pipeline/
│   ├── extract.py       # PDF text extraction
│   ├── chunk.py         # Chunking logic
│   ├── embed.py         # Embedding via Ollama
│   └── store.py         # pgvector storage
├── chatbot/
│   ├── retrieve.py      # Semantic search
│   ├── generate.py      # LLM response generation
│   └── guardrails.py    # Hallucination prevention
├── main.py              # Run full pipeline
└── README.md
```

---

## Notes

- All processing is **local** — Ollama runs the LLM and embeddings on your machine, no data leaves your system
- Data is sourced strictly from EPFO's official website to ensure accuracy
- Guardrails will be added in the next phase to restrict the chatbot to only answer from the stored knowledge base
