import os
import joblib
import shutil
import PyPDF2
from fastapi import FastAPI, UploadFile, File
from config import UPLOADS_DIR, BEST_MODEL_PATH, SELECTED_FEATURES_PATH, TFIDF_VECTOR_PATH
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import csr_matrix

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Load Model & Feature Selector
print(" Loading Model & Feature Selector...")
model = joblib.load(BEST_MODEL_PATH)
selected_features = joblib.load(SELECTED_FEATURES_PATH)
tfidf_vectorizer = joblib.load(TFIDF_VECTOR_PATH)

# ✅ Function to extract text from uploaded resume
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + " "
    return text.strip()

# ✅ Upload Resume Endpoint
@app.post("/upload_resume/")
async def upload_resume(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOADS_DIR, file.filename)

    # ✅ Save uploaded
    # file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Extract text from PDF
    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            resume_text = f.read()

    return {"filename": file.filename, "extracted_text": resume_text}
