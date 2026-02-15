# backend/jobsuggest.py

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import logging
from backend.models.resume_parser import extract_text_from_pdf
from backend.models.groq_llm import suggest_top_jobs_from_resume  # You'll create this

router = APIRouter()
UPLOAD_FOLDER = "backend/models/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/suggest-jobs/")
async def suggest_jobs(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        resume_text = extract_text_from_pdf(file_path)
        result = suggest_top_jobs_from_resume(resume_text)

        return JSONResponse(content={"jobs": result}, status_code=200)
    except Exception as e:
        logging.exception("Job suggestion failed")
        raise HTTPException(status_code=500, detail=str(e))
