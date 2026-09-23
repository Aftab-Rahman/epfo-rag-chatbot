from dotenv import load_dotenv
import os
import re

import streamlit as st
import psycopg
import ollama
from sentence_transformers import SentenceTransformer

load_dotenv()  # Load environment variables from .env file

# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="RAG Chatbot",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 RAG Chatbot")
st.caption("Ask questions about the documents in the knowledge base.")


# -----------------------------
# Load embedding model once
# -----------------------------

@st.cache_resource
def load_embedding_model():
    return SentenceTransformer("all-MiniLM-L6-v2")


model = load_embedding_model()


# -----------------------------
# Search PostgreSQL
# -----------------------------

def search_documents(query, top_k=5):

    query_embedding = model.encode(query).tolist()

    conn = psycopg.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT content, source, page_number,
               embedding <=> %s::vector AS distance
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s;
        """,
        (query_embedding, query_embedding, top_k)
    )

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


# -----------------------------
# Generate answer
# -----------------------------

def generate_answer(query, results):

    context = ""

    for i, (content, source, page_number, distance) in enumerate(
        results, start=1
    ):
        context += f"""
[SOURCE {i}]
Source: {source}
Page: {page_number}
Content:
{content}

"""

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
                    "Do not add a separate 'According to' paragraph that repeats "
                    "the answer. "
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
"""
            }
        ]
    )

    return response["message"]["content"]


# -----------------------------
# Chat interface
# -----------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# User input

query = st.chat_input("Ask a question about your documents...")


if query:

    # Display user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )

    with st.chat_message("user"):
        st.markdown(query)

    # Generate answer
    with st.chat_message("assistant"):

        with st.spinner("Searching documents and generating answer..."):

            results = search_documents(query)

            answer = generate_answer(query, results)

        st.markdown(answer)

        # -----------------------------
        # Display cited sources
        # -----------------------------

        cited_numbers = set(
            int(number)
            for number in re.findall(r"\[SOURCE (\d+)\]", answer)
        )

        if cited_numbers:

            st.markdown("### Sources")

            for number in sorted(cited_numbers):

                if 1 <= number <= len(results):

                    content, source, page_number, distance = results[number - 1]

                    if page_number:
                        st.markdown(
                            f"**[SOURCE {number}]** — "
                            f"{source}, Page {page_number}"
                        )
                    else:
                        st.markdown(
                            f"**[SOURCE {number}]** — {source}"
                        )

    # Save assistant response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )