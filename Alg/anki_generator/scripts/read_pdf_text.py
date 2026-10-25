import os
import pypdf
import sys

def extract_pdf_text(pdf_path):
    try:
        reader = pypdf.PdfReader(pdf_path)
        text = ""
        for i, page in enumerate(reader.pages):
            text += f"--- Page {i+1} ---\n"
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error reading {pdf_path}: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python read_pdf_text.py <path_to_pdf>")
        sys.exit(1)
    
    # Reconfigure stdout to use utf-8
    sys.stdout.reconfigure(encoding='utf-8')
    pdf_path = sys.argv[1]
    print(extract_pdf_text(pdf_path))
