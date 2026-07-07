import os
import fitz
from docx import Document as DocxDocument

from langchain_core.documents import Document

from utils.text_cleaner import clean_text


def load_pdf_documents(pdf_folder):
    documents = []

    for root, _, files in os.walk(pdf_folder):
        for file in files:
            if file.endswith(".pdf"):
                path = os.path.join(root, file)

                pdf = fitz.open(path)

                for page_num, page in enumerate(pdf, start=1):
                    text = clean_text(page.get_text())

                    if text:
                        documents.append(
                            Document(
                                page_content=text,
                                metadata={
                                    "source": file,
                                    "page": page_num,
                                    "type": "pdf"
                                }
                            )
                        )

                pdf.close()

    return documents


def load_docx_documents(doc_folder):
    documents = []

    for root, _, files in os.walk(doc_folder):
        for file in files:
            if file.endswith(".docx"):
                path = os.path.join(root, file)

                doc = DocxDocument(path)

                text = "\n".join(
                    clean_text(p.text)
                    for p in doc.paragraphs
                    if clean_text(p.text)
                )

                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": file,
                            "type": "docx"
                        }
                    )
                )

    return documents