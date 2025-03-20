import os
import joblib
import shutil
import PyPDF2
from fastapi import FastAPI, UploadFile, File, Form
from config import UPLOADS_DIR, BEST_MODEL_PATH, SELECTED_FEATURES_PATH, TFIDF_VECTOR_PATH
from predict_category import predict_category

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Load Model & Feature Selector
print("🚀 Loading Model & Feature Selector...")
model = joblib.load(BEST_MODEL_PATH)
selected_features = joblib.load(SELECTED_FEATURES_PATH)
tfidf_vectorizer = joblib.load(TFIDF_VECTOR_PATH)

# ✅ Ensure upload directory exists
os.makedirs(UPLOADS_DIR, exist_ok=True)

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

    # ✅ Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # ✅ Extract text from PDF
    if file.filename.endswith(".pdf"):
        resume_text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            resume_text = f.read()

    return {"filename": file.filename, "extracted_text": resume_text}

# ✅ API Route to Predict Job Category from PDF or Text
@app.post("/predict_category/")
async def predict_category_api(file: UploadFile = File(None), text: str = Form(None)):
    # Ensure at least one input method is provided
    if not file and not text:
        return {"error": "Please provide either a resume file or text input."}
    
    # If PDF is uploaded, extract text
    if file:
        pdf_reader = PyPDF2.PdfReader(file.file)
        text = " ".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])

    # Get prediction results
    predictions = predict_category(text)

    return {"Top Predicted Categories": predictions}

# ✅ Root Endpoint
@app.get("/")
def home():
    return {"message": "Welcome to Resume Optimizer API! 🎯"}
