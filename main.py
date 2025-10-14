from fastapi import FastAPI, Request
from anthropic import Anthropic
import os
import json
import httpx

app = FastAPI()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# This will be your ngrok URL - update after ngrok is running
LOCAL_JOB_API = os.getenv("LOCAL_JOB_API_URL", "http://localhost:8001")

@app.post("/omi/webhook")
async def omi_webhook(request: Request):
    try:
        data = await request.json()
        
        # Extract transcript from Omi payload
        segments = data.get("segments", [])
        session_id = data.get("session_id", "")
        
        # Combine segments into full transcript
        full_transcript = " ".join([seg.get("text", "") for seg in segments])
        
        print(f"📝 Received transcript: {full_transcript}")
        
        # Check if it's a job application command
        if "apply" in full_transcript.lower() and ("job" in full_transcript.lower() or "career" in full_transcript.lower() or "http" in full_transcript.lower() or "slash" in full_transcript.lower() or "dot" in full_transcript.lower()):
            
            print("✅ Job application detected! Extracting URL...")
            
            # Use Claude to extract and normalize the URL
            response = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": f"""Extract and normalize the job URL from this transcript: "{full_transcript}"

Convert voice to URL:
- "basedhardware dot com slash pages slash careers" → "https://basedhardware.com/pages/careers"
- "omi dot me slash careers" → "https://omi.me/careers"
- "google slash careers" → "https://google.com/careers"

Add https:// if missing.

Respond ONLY with the URL, nothing else."""
                }]
            )
            
            job_url = response.content[0].text.strip()
            print(f"🔗 Extracted URL: {job_url}")
            
            # Call local job automator API
            try:
                async with httpx.AsyncClient(timeout=60.0) as http_client:
                    api_response = await http_client.post(
                        f"{LOCAL_JOB_API}/api/apply-to-job",
                        json={"url": job_url}
                    )
                    result = api_response.json()
                
                # Send notification to Omi
                notification_text = f"""✅ Job Application Started!

Company: {result.get('company', 'Unknown')}
Role: {result.get('job_title', 'Unknown')}
Fields Found: {result.get('total_fields', 0)}

Browser opened on your computer for review!"""
                
                return {
                    "notification": {
                        "title": "Job Application In Progress 🎯",
                        "body": notification_text
                    }
                }
                
            except Exception as api_error:
                print(f"❌ Error calling job API: {api_error}")
                return {
                    "notification": {
                        "title": "Error ❌",
                        "body": f"Could not process job application: {str(api_error)}"
                    }
                }
        
        return {"status": "not_a_job_command", "transcript": full_transcript}
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e)}

@app.get("/")
async def root():
    return {
        "app": "Omi Job Assistant", 
        "status": "running",
        "local_api": LOCAL_JOB_API
    }

@app.get("/health")
async def health():
    # Check if local API is reachable
    try:
        async with httpx.AsyncClient(timeout=5.0) as http_client:
            response = await http_client.get(f"{LOCAL_JOB_API}/health")
            local_api_status = "connected" if response.status_code == 200 else "error"
    except:
        local_api_status = "disconnected"
    
    return {
        "status": "healthy",
        "local_api_status": local_api_status,
        "local_api_url": LOCAL_JOB_API
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)