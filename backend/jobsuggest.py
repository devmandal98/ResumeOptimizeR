from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
import shutil
import requests
import logging
from dotenv import load_dotenv
from pathlib import Path
from backend.models.resume_parser import extract_text_from_pdf
from backend.models.groq_llm import get_job_search_query

# --- BEN'S UNIVERSAL PATH FIX ---
# This checks the current folder AND the parent folder for the .env
current_dir = Path(__file__).resolve().parent
env_locations = [current_dir / ".env", current_dir.parent / ".env"]

for loc in env_locations:
    if loc.exists():
        load_dotenv(dotenv_path=loc)
        break
# --------------------------------

router = APIRouter()
UPLOAD_FOLDER = os.path.join("backend", "models", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/suggest-jobs/")
async def suggest_jobs(file: UploadFile = File(...)):
    try:
        # 1. Save and Parse Resume
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
        
        resume_text = extract_text_from_pdf(file_path)

        # 2. Get the "Search Term" from AI
        raw_query = get_job_search_query(resume_text)
        # Ensure it's a clean, single-line string
        search_query = str(raw_query).strip().replace("\n", " ")

        # 3. Call Adzuna API
        app_id = os.getenv("ADZUNA_APP_ID")
        app_key = os.getenv("ADZUNA_APP_KEY")

        # Log check to your terminal (to see if keys are actually loading)
        if not app_id or not app_key:
            logging.error(f"Environment Error: ADZUNA_APP_ID: {app_id}, ADZUNA_APP_KEY: {app_key}")
            raise ValueError("ADZUNA credentials missing in .env. Ensure they are in backend/.env")

        country = "in" # Change to 'us' or 'gb' as needed
        url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/1"
        
        # We explicitly cast everything to str and remove any potential hidden characters
        params = {
            "app_id": str(app_id).strip(),
            "app_key": str(app_key).strip(),
            "results_per_page": 10,
            "what": str(search_query),
            "content-type": "application/json"
        }

        # 4. Execute Request
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code != 200:
            # This will show the exact reason Adzuna is rejecting you
            error_detail = response.text
            logging.error(f"Adzuna API Error ({response.status_code}): {error_detail}")
            return JSONResponse(content={"error": f"Adzuna rejection: {error_detail}"}, status_code=500)

        data = response.json()
        raw_jobs = data.get("results", [])
        
        # 5. Clean the data for the Frontend
        formatted_jobs = []
        for job in raw_jobs:
            # Adzuna uses nested dictionaries for company and location
            company_info = job.get("company", {})
            location_info = job.get("location", {})
            
            formatted_jobs.append({
                "title": job.get("title", "Job Opportunity").replace("<strong>", "").replace("</strong>", ""),
                "company": company_info.get("display_name", "Company Confidential"),
                "location": location_info.get("display_name", "Remote/Not Specified"),
                "link": job.get("redirect_url"),
                "description": job.get("description", "No description provided.").replace("<strong>", "").replace("</strong>", "")
            })

        return JSONResponse(content={"jobs": formatted_jobs}, status_code=200)

    except Exception as e:
        logging.exception("Job suggestion process failed")
        return JSONResponse(content={"error": str(e)}, status_code=500)