import os
from pdfminer.high_level import extract_text

# Folder where PDF resumes are stored (inside 'data/')
pdf_folder_path = "data/"

# Function to extract text from a single PDF
def extract_text_from_pdf(pdf_path):
    try:
        text = extract_text(pdf_path)
        return text.strip()
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
        return None

# Process all PDFs in each category folder
all_resumes = {}  # Dictionary to store {filename: text}

for category in os.listdir(pdf_folder_path):
    category_path = os.path.join(pdf_folder_path, category)
    
    if os.path.isdir(category_path):  # Check if it's a folder
        for pdf_file in os.listdir(category_path):
            if pdf_file.endswith(".pdf"):
                pdf_path = os.path.join(category_path, pdf_file)
                print(f"Extracting text from: {pdf_path}")
                
                text = extract_text_from_pdf(pdf_path)
                if text:
                    all_resumes[pdf_file] = text

# Save extracted text as a new file (optional)
with open("extracted_resumes.txt", "w", encoding="utf-8") as f:
    for filename, text in all_resumes.items():
        f.write(f"Resume: {filename}\n{text}\n\n")
                
print("✅ PDF text extraction complete!")
