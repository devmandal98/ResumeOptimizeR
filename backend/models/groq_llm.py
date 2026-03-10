import os
import requests
from dotenv import load_dotenv
from pathlib import Path

# Fix: Ensure .env is loaded even when running from root
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

def get_job_search_query(resume_text: str):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Software Engineer" # Fallback if key is missing

    prompt = f"""
    Analyze the following resume and generate a short search query (3-5 words) 
    for a job board. Focus on strongest technical skills.
    Return ONLY the keywords. No quotes, no explanation.
    
    Resume:
    {resume_text}
    """

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
        res_data = response.json()
        
        if "choices" in res_data:
            query = res_data["choices"][0]["message"]["content"]
            # Force result to be a clean string
            return str(query).strip().replace('"', '')
        return "Software Engineer"
    except Exception as e:
        print(f"Groq Error: {e}")
        return "Software Engineer"