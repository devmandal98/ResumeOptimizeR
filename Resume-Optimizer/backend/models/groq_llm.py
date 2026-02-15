import os
import requests

def suggest_top_jobs_from_resume(resume_text: str):
    prompt = f"""
You are an AI career advisor.

A user uploaded the following resume. Analyze the resume deeply and suggest the top 10 job roles the candidate is best suited for based on their skills, experience, and interests.

For each job role, return:
1. Job Title
2. Match Score (as a percentage)
3. One-line explanation

Resume:
\"\"\"
{resume_text}
\"\"\"
"""

    headers = {
        "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload)
    content = response.json()["choices"][0]["message"]["content"]
    return content.strip()
