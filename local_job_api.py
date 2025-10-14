from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add job automator to path
job_automator_path = r"C:\Users\AjayNelavetla\OneDrive - Folderwave, Inc\Desktop\Job Application Bot\job-application-automator-main\job-application-automator-main"
sys.path.insert(0, job_automator_path)

from job_application_automator.form_extractor import SimpleFormExtractor

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/apply-to-job")
async def apply_to_job(data: dict):
    try:
        url = data.get("url")
        
        if not url:
            raise HTTPException(status_code=400, detail="URL required")
        
        print(f"🎯 Applying to job at: {url}")
        
        # Extract form
        print("📋 Extracting form fields...")
        extractor = SimpleFormExtractor()
        form_data = await extractor.extract_form_data(url)
        
        print(f"✅ Found {form_data.get('total_fields')} fields")
        
        return {
            "status": "extracted",
            "message": f"Extracted {form_data.get('total_fields')} fields",
            "job_title": form_data.get('job_title'),
            "company": form_data.get('company'),
            "total_fields": form_data.get('total_fields')
        }
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"app": "Local Job Automator API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Local Job Automator API...")
    print("📍 http://localhost:8001")
    uvicorn.run(app, host="0.0.0.0", port=8001)