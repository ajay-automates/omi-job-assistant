from fastapi import FastAPI, Request
from anthropic import Anthropic
import os

app = FastAPI()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# Simulated Omi webhook receiver
@app.post("/omi/webhook")
async def omi_webhook(request: Request):
    data = await request.json()
    transcript = data.get("transcript", "")
    
    # Check if it's a job application command
    if "apply" in transcript.lower() and ("job" in transcript.lower() or "http" in transcript):
        # Extract URL from transcript using Claude
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": f"""Extract the job URL from this text: "{transcript}"
                
                Respond with JSON:
                {{"url": "extracted_url", "company": "company_name"}}
                
                If no URL found, return null."""
            }]
        )
        
        result = response.content[0].text
        
        # Here you'd call your existing job automator tools
        # For now, just return success
        return {
            "status": "success",
            "message": f"Would apply to job using your existing tools",
            "transcript": transcript,
            "parsed": result,
            "notification": "Job application submitted! 🎉"
        }
    
    return {"status": "not_a_job_command"}

@app.get("/")
async def root():
    return {"app": "Omi Job Assistant", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)