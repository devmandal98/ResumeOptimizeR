import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from pathlib import Path

# --- BEN'S UNIVERSAL PATH FIX ---
# This looks for the .env file exactly where it lives (inside the backend folder)
# even if you run uvicorn from the root folder.
current_file_path = Path(__file__).resolve()
backend_dir = current_file_path.parent
env_path = backend_dir / ".env"

load_dotenv(dotenv_path=env_path)
# --------------------------------

router = APIRouter(tags=["chatbot"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # 1. Verify API Key exists
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print(f"DEBUG ERROR: API Key not found at {env_path}")
        raise HTTPException(
            status_code=500, 
            detail="GROQ_API_KEY is missing. Please check your backend/.env file."
        )

    # 2. Craft the prompt
    prompt = f"""
You are an expert career advisor chatbot.  
User: "{request.message}"
Provide clear, actionable career guidance in your reply.
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    payload = {
        "model": "llama-3.3-70b-versatile", # Updated model name
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        # 3. Call Groq API
        resp = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30,
        )
        
        # 4. Handle API Response safely
        res_data = resp.json()

        if resp.status_code != 200:
            print(f"GROQ API ERROR: {res_data}")
            raise HTTPException(status_code=resp.status_code, detail="AI service error")

        # 5. Check if 'choices' exists before accessing (Prevents KeyError)
        if "choices" in res_data and len(res_data["choices"]) > 0:
            content = res_data["choices"][0]["message"]["content"].strip()
            return ChatResponse(reply=content)
        else:
            raise HTTPException(status_code=500, detail="Malformed response from AI service")

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="AI service request timed out")
    except Exception as e:
        print(f"INTERNAL ERROR: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")