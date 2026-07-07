import fitz
import os
from utils.text_cleaner import clean_text

PDF_FOLDER = "Data/pdfs"
OUTPUT_FILE = "output/raw_text.txt"

all_text = ""

for root, dirs, files in os.walk(PDF_FOLDER):
    for file in files:
        if file.endswith(".pdf"):
            pdf_path = os.path.join(root, file)
            print(f"Processing: {pdf_path}")

            doc = fitz.open(pdf_path)
            print("Pages:", len(doc))

            for page in doc:
                text = clean_text(page.get_text())
                print(f"Page {page.number + 1}: {len(text)} characters")
                all_text += text + "\n"

            doc.close()
# Save output
os.makedirs("output", exist_ok=True)

print("Saving to:")
print(os.path.abspath(OUTPUT_FILE))

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(all_text)

print("✅ All PDFs from all folders processed!")