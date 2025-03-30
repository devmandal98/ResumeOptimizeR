from fastapi import FastAPI, UploadFile, File, HTTPException
from pdfminer.high_level import extract_text

app = FastAPI()

# ✅ Function to extract text using pdfminer.six
def extract_pdf_text(pdf_file):
    try:
        text = extract_text(pdf_file)  # Extract text from the PDF

        if not text.strip():  
            raise HTTPException(status_code=400, detail="No readable text found in PDF.")

        return text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting text: {str(e)}")

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        text = extract_pdf_text(file.file)

        return {
            "message": "PDF uploaded successfully!",
            "text_preview": text[:2000]  # Show first 2000 characters
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
