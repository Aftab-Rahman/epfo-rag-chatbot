from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.document_loader import (
    load_pdf_documents,
    load_docx_documents,
)

# Load documents
documents = []

#documents.extend(load_pdf_documents("Data/pdfs"))
#pdf is faded so it can majorly consider faqs, as facing pprblem with huge data
documents.extend(load_docx_documents("Data/docs"))

print(f"Loaded {len(documents)} documents.")

# Create splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# Split into chunks
chunks = splitter.split_documents(documents)

print(f"Created {len(chunks)} chunks.")

# Save chunks (for inspection only)
with open("output/chunks.txt", "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks, start=1):
        f.write(f"\n{'='*80}\n")
        f.write(f"Chunk {i}\n")
        f.write(f"Metadata: {chunk.metadata}\n\n")
        f.write(chunk.page_content)
        f.write("\n")

print("✅ Chunks saved to output/chunks.txt")
