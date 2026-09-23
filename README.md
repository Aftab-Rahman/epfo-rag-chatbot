Great. Let's do it in a controlled way.

I'll draft the **current README based on the original structure you showed me and the implementation we've completed**, rather than changing anything in your project yet.

### Current README — replacement draft

````markdown
# RAG Chatbot — Provident Fund (EPFO)

A Retrieval-Augmented Generation (RAG) chatbot designed to answer questions about India's Provident Fund (PF) using a curated knowledge base sourced from EPFO-related documents.

The system retrieves relevant document content before generating an answer, helping keep responses grounded in the available knowledge base. Retrieved sources are included with the response so users can see where the information came from.

---

## Project Overview

This project implements a local RAG-based chatbot for answering questions related to Provident Fund and EPFO information.

Instead of asking an LLM to answer questions from its general knowledge alone, the system follows a retrieval-first approach:

```text
User Question
      ↓
Question Embedding
      ↓
Semantic Search
      ↓
PostgreSQL + pgvector
      ↓
Top 5 Relevant Document Chunks
      ↓
Ollama / llama3.2
      ↓
Grounded Answer + Source Citations
      ↓
Streamlit Chat Interface
````

The goal is to make answers traceable to the retrieved source material and reduce unsupported or hallucinated responses.

---

## Features

* Retrieval-Augmented Generation (RAG)
* Semantic similarity search using vector embeddings
* PostgreSQL database with pgvector
* Local embedding generation
* Local LLM inference through Ollama
* Top-5 document retrieval
* Source-aware answers using `[SOURCE X]` citations
* Streamlit-based chat interface
* Environment-variable based database configuration
* Conversation history within the Streamlit session
* Grounded-response instructions for the LLM

---

## Technology Stack

| Component               | Technology            |
| ----------------------- | --------------------- |
| Programming Language    | Python                |
| User Interface          | Streamlit             |
| Embedding Model         | `all-MiniLM-L6-v2`    |
| Embedding Library       | Sentence Transformers |
| Vector Database         | PostgreSQL + pgvector |
| LLM Runtime             | Ollama                |
| LLM                     | `llama3.2`            |
| Database Driver         | Psycopg 3             |
| Configuration           | python-dotenv         |
| Version Control         | Git + GitHub          |
| Development Environment | VS Code               |

---

## RAG Pipeline

### 1. Document Processing

Source documents are extracted and processed before being added to the knowledge base.

The processing pipeline includes:

```text
Documents
   ↓
Text Extraction
   ↓
Text Cleaning
   ↓
Chunking
   ↓
Embedding Generation
   ↓
PostgreSQL + pgvector
```

The project stores document content together with metadata such as the source and page number where available.

Page/source information is retained so that retrieved content can later be referenced in chatbot responses.

---

### 2. Text Chunking

Large documents are divided into smaller chunks.

Chunking makes it possible to retrieve the portions of a document that are most relevant to a user's question instead of passing an entire document to the LLM.

The project uses overlapping chunks so that information near chunk boundaries is less likely to be separated from related context.

---

### 3. Embeddings

The project uses:

```text
all-MiniLM-L6-v2
```

through the Sentence Transformers library.

The model converts text into numerical vectors representing semantic information.

The same embedding model is used for both:

* document chunks
* user questions

This allows the system to compare the semantic similarity between a question and stored document chunks.

The model produces **384-dimensional embeddings**.

---

### 4. PostgreSQL + pgvector

The generated embeddings are stored in PostgreSQL using the `pgvector` extension.

The database contains the document content, metadata, and vector embeddings required for semantic retrieval.

Conceptually:

```text
Document Chunk
      +
Source
      +
Page Number
      +
Embedding
      ↓
PostgreSQL
      ↓
pgvector similarity search
```

The project currently retrieves the **top 5 most relevant chunks** for each user question.

---

## Retrieval

When a user asks a question, the question is converted into an embedding using the same `all-MiniLM-L6-v2` model.

The vector is then compared with the embeddings stored in PostgreSQL.

The system uses vector distance to identify the most semantically relevant document chunks.

The current retrieval query returns:

```text
Top 5 relevant chunks
```

along with:

* document content
* source
* page number
* similarity distance

These retrieved chunks become the context supplied to the LLM.

---

## Answer Generation

The retrieved chunks are passed to the local Ollama model:

```text
llama3.2
```

The LLM is instructed to answer using the retrieved context rather than relying on unsupported information.

The context is presented using source labels such as:

```text
[SOURCE 1]
[SOURCE 2]
[SOURCE 3]
...
```

The model is instructed to:

* use the provided context
* cite factual claims using valid source numbers
* avoid inventing source references
* indicate when the available context is insufficient

This provides a grounding mechanism between retrieval and answer generation.

---

## Source Citations

The chatbot supports source citations in generated answers.

For example:

```text
According to [SOURCE 1], ...
```

The Streamlit interface parses these source references and displays a separate **Sources** section.

Example:

```text
Sources

[SOURCE 1] — PF FAQ's.docx
```

Where page information is available, it can also be displayed with the source.

This makes the generated response more traceable to the retrieved knowledge base.

---

## Streamlit Interface

The chatbot includes a Streamlit web interface.

The interface provides:

* Chat-style interaction
* User question input
* Generated answers
* Source references
* Conversation history during the current session

Run the application with:

```powershell
streamlit run app.py
```

The application can then be opened in a browser using the local Streamlit address provided by the terminal.

---

## Environment Configuration

Database credentials are kept outside the source code using a `.env` file.

Example:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=chatbot_db
DB_USER=postgres
DB_PASSWORD=your_password
```

The application loads these values using `python-dotenv`.

### Important

The `.env` file should **never be committed to Git**.

It is excluded through `.gitignore`.

A safe repository should contain the configuration structure, but not the actual database password.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Aftab-Rahman/epfo-rag-chatbot.git
cd epfo-rag-chatbot
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

---

## Required Services

The application requires:

### PostgreSQL

PostgreSQL is used as the primary database.

### pgvector

The PostgreSQL `vector` extension is required for storing and searching embeddings.

Example:

```sql
CREATE EXTENSION IF NOT EXISTS vector;
```

### Ollama

Ollama is used to run the LLM locally.

The project currently uses:

```text
llama3.2
```

Make sure the model is available in Ollama before running the chatbot.

---

## Running the Project

After configuring PostgreSQL, pgvector, Ollama, and the `.env` file:

```powershell
streamlit run app.py
```

The Streamlit application will start locally.

---

## Project Structure

The current project structure includes:

```text
Project - chatbot/
│
├── app.py
├── database.py
├── test_db_connection.py
├── requirements.txt
├── .gitignore
│
├── db/
│   └── database.py
│
├── scripts/
│   ├── chunk_documents.py
│   ├── extract_docx.py
│   ├── extract_text.py
│   ├── generate_embeddings.py
│   ├── search.py
│   ├── store_embeddings.py
│   └── search_backup.py
│
└── utils/
    ├── document_loader.py
    ├── text_cleaner.py
    └── __init__.py
```

> `search_backup.py` is currently kept locally as an untracked backup file and is not part of the Git repository.

---

## Core Components

### `app.py`

Provides the Streamlit user interface and connects the complete RAG workflow to the chat interface.

### `scripts/generate_embeddings.py`

Generates vector embeddings for processed document chunks using `all-MiniLM-L6-v2`.

### `scripts/store_embeddings.py`

Stores document chunks and their embeddings in PostgreSQL.

### `scripts/search.py`

Performs semantic retrieval and sends the retrieved context to Ollama for answer generation.

### `scripts/chunk_documents.py`

Creates smaller document chunks suitable for embedding and retrieval.

### `scripts/extract_text.py`

Handles text extraction from supported source material.

### `utils/text_cleaner.py`

Contains text-cleaning functionality used during document preparation.

---

## Current Retrieval Configuration

The current retrieval system uses:

```text
Embedding model:
all-MiniLM-L6-v2

Vector database:
PostgreSQL + pgvector

Retrieved chunks:
Top 5

LLM:
Ollama llama3.2
```

The same embedding model must be used consistently when generating document embeddings and embedding user queries.

---

## Grounding and Hallucination Control

A key objective of this project is to keep generated responses grounded in the retrieved knowledge base.

The system therefore:

1. Retrieves relevant document chunks.
2. Passes only the retrieved context to the answer-generation stage.
3. Labels retrieved context with source identifiers.
4. Instructs the LLM to cite factual claims.
5. Requires valid source numbers.
6. Instructs the model to acknowledge when the available context is insufficient.

These measures reduce the likelihood of unsupported answers, although no LLM-based system can guarantee that hallucinations will never occur.

---

## Data Source

The project is focused on Provident Fund / EPFO-related information.

The knowledge base is built from project source documents containing EPFO/PF information.

Source and page metadata are retained where available so retrieved information can be traced back to its originating document.

---

## Limitations

The current system has several practical limitations:

* Answer quality depends on the quality of the source documents.
* Retrieval quality depends on chunking and embedding quality.
* The LLM may still generate incorrect information despite grounding instructions.
* Only information available in the indexed knowledge base can reliably be retrieved.
* Local LLM performance depends on the available hardware.
* The current retrieval configuration uses a fixed top-5 result count.

---

## Future Improvements

Possible future improvements include:

* Improving document preprocessing
* Experimenting with different chunk sizes
* Adding metadata filtering
* Improving retrieval/ranking
* Adding reranking
* Evaluating different embedding models
* Adding automated RAG evaluation
* Improving citation handling
* Adding document management functionality
* Improving UI/UX
* Adding deployment support
* Adding automated tests
* Measuring retrieval and response latency

---

## Development Status

The project currently has a working RAG pipeline with:

* Document processing
* Chunking
* Embedding generation
* PostgreSQL + pgvector storage
* Semantic retrieval
* Local LLM generation
* Source citations
* Streamlit chat interface
* Environment-based database configuration

The project is continuing to evolve as retrieval quality, evaluation, documentation, and deployment are improved.

---

## License

This project is intended for educational and development purposes.

Refer to the repository for the applicable project license and source-data terms.

````

### Important correction from the old README

I deliberately changed the old architecture from:

```text
Ollama → nomic-embed-text → 768 dimensions
````

to your **actual current architecture**:

```text
Sentence Transformers
        ↓
all-MiniLM-L6-v2
        ↓
384-dimensional embeddings
        ↓
PostgreSQL + pgvector
```

That is an important distinction because mixing those two embedding models would make the documented architecture inconsistent with the database embeddings you're actually using.

Also, I have **not claimed things we haven't actually implemented**, such as reranking, automated evaluation, or deployment.
