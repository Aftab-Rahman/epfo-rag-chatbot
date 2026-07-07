from docx import Document
import os
from utils.text_cleaner import clean_text

DOC_FOLDER = "Data/docs"
OUTPUT_FILE = "output/doc_text.txt"

all_text = ""

for root, dirs, files in os.walk(DOC_FOLDER):
    for file in files:
        if file.endswith(".docx"):
            doc_path = os.path.join(root, file)
            print(f"Processing: {doc_path}")

            doc = Document(doc_path)

            all_text += f"\n{'='*60}\n"
            all_text += f"FILE: {file}\n"
            all_text += f"{'='*60}\n\n"

            print(f"Total paragraphs: {len(doc.paragraphs)}")
            
            for para in doc.paragraphs:
                text = clean_text(para.text)

                if text:
                    all_text += text + "\n"

os.makedirs("output", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(all_text)

print("✅ DOCX extraction completed!")