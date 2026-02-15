from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import os, shutil, logging, sys

# ensure import of your models directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'models')))

from backend.models.pdf_converter import pdf_to_markdown, save_markdown_to_file, markdown_to_pdf
from backend.models.llm import generate_optimized_resume
from backend.auth import router as auth_router  # Import auth router
from backend.jobsuggest import router as jobsuggest_router #import job suggest fastapi router
from backend.chatbot import router as chatbot_router # import chatbot fastapi router

app = FastAPI()
# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1) Include auth endpoints before other routes
app.include_router(auth_router)

# Include Job Suggest Router
app.include_router(jobsuggest_router)

app.include_router(chatbot_router)# chatbot router

# 2) Define upload endpoint before mounting static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "backend", "models")
UPLOAD_DIR = os.path.join(MODELS_DIR, "uploads")
OUTPUT_DIR = os.path.join(MODELS_DIR, "outputs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/upload/")
async def upload_and_download_resume(
    file: UploadFile = File(...),
    job_description: str = Form(...),
    # if you add authentication, you can depend on a token here
):
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        logger.info(f"Uploaded '{file.filename}'")
        md = pdf_to_markdown(file_location)
        optimized = generate_optimized_resume(md, job_description)
        md_file = save_markdown_to_file(optimized, "Optimized_Resume.md")
        pdf_out = os.path.join(OUTPUT_DIR, "Formatted_Resume.pdf")
        markdown_to_pdf(md_file, pdf_out)

        return FileResponse(
            path=pdf_out,
            filename="Optimized_Resume.pdf",
            media_type="application/pdf"
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# 3) Mount frontend folder for static files and SPA fallback last
app.mount(
    "/",
    StaticFiles(directory="frontend", html=True),
    name="frontend",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
