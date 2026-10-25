import os
import pypdf
import json

def extract_all_pdfs():
    base_dir = "C:\\Users\\lovek\\Documents\\EX\\Alg"
    output_dir = os.path.join(base_dir, "anki_generator", "extracted_text")
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = []
    # Walk the directory to find all PDFs
    for root, dirs, files in os.walk(base_dir):
        # Exclude anki_generator directory itself and other non-exercise directories
        if "anki_generator" in root or ".git" in root or "aa-ics-s26-connect-four" in root:
            continue
        for file in files:
            if file.endswith(".pdf"):
                pdf_files.append(os.path.join(root, file))
                
    summary = []
    for pdf_path in pdf_files:
        rel_path = os.path.relpath(pdf_path, base_dir)
        try:
            reader = pypdf.PdfReader(pdf_path)
            text = ""
            for i, page in enumerate(reader.pages):
                text += f"--- Page {i+1} ---\n"
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            # Save to a text file
            safe_name = rel_path.replace(os.sep, "_").replace(".pdf", ".txt")
            txt_path = os.path.join(output_dir, safe_name)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text)
                
            summary.append({
                "pdf": rel_path,
                "txt": safe_name,
                "pages": len(reader.pages),
                "chars": len(text)
            })
        except Exception as e:
            summary.append({
                "pdf": rel_path,
                "error": str(e)
            })
            
    # Write summary report
    summary_path = os.path.join(output_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Extracted {len(summary)} PDFs. Summary saved to {summary_path}")
    for item in summary:
        if "error" in item:
            print(f"FAILED: {item['pdf']} - {item['error']}")
        else:
            print(f"SUCCESS: {item['pdf']} ({item['pages']} pages, {item['chars']} chars)")

if __name__ == "__main__":
    extract_all_pdfs()
