# backend/chatbot.py
import os
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["chatbot"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@router.post("/chat/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # craft a prompt for career advice
    prompt = f"""
You are an expert career advisor chatbot.  
User: "{request.message}"
Provide clear, actionable career guidance in your reply.
"""
    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": prompt}],
    }
    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=payload,
        timeout=30,
    )
    if not resp.ok:
        raise HTTPException(status_code=500, detail="AI service error")
    content = resp.json()["choices"][0]["message"]["content"].strip()
    return ChatResponse(reply=content)
