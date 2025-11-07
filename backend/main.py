"""
FastAPI Backend for CredibleMe
Handles credential verification requests and serves web pages
"""
from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Optional
from gemini_client import GeminiClient
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="CredibleMe",
    description="Privacy-friendly credential verification using Gemini AI",
    version="1.0.0"
)

# Setup templates and static files
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

# Create directories if they don't exist
TEMPLATES_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# Initialize Gemini client
gemini_client = GeminiClient()

# In-memory storage (session-based, no persistence)
session_storage = {}


# Request/Response models
class VerifyRequest(BaseModel):
    """Request model for credential verification"""
    resume_text: str
    github_username: str
    linkedin_url: str


class VerifyResponse(BaseModel):
    """Response model for verification results"""
    trust_score: int
    reasoning: str
    badge: str
    session_id: Optional[str] = None


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Landing page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/verify", response_class=HTMLResponse)
async def verify_page(request: Request):
    """Verification form page"""
    return templates.TemplateResponse("verify.html", {"request": request})


@app.get("/result/{session_id}", response_class=HTMLResponse)
async def result_page(request: Request, session_id: str):
    """Result display page"""
    if session_id not in session_storage:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": "Session not found. Please verify your credentials again."
            }
        )
    
    result = session_storage[session_id]
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            "trust_score": result["trust_score"],
            "reasoning": result["reasoning"],
            "badge": result["badge"],
            "session_id": session_id
        }
    )


@app.post("/verify")
async def verify_credentials_form(
    request: Request,
    resume_text: str = Form(...),
    github_username: str = Form(...),
    linkedin_url: str = Form(...)
):
    """
    Verify user credentials using Gemini AI (form submission)
    
    Args:
        request: FastAPI Request object
        resume_text: Resume content
        github_username: GitHub username
        linkedin_url: LinkedIn URL
        
    Returns:
        Redirect to result page
    """
    try:
        # Validate input
        if not resume_text.strip():
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "error": "Resume text is required"
                }
            )
        
        if not github_username.strip():
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "error": "GitHub username is required"
                }
            )
        
        if not linkedin_url.strip():
            return templates.TemplateResponse(
                "error.html",
                {
                    "request": request,
                    "error": "LinkedIn URL is required"
                }
            )
        
        # Call Gemini for analysis
        result = gemini_client.analyze_credentials(
            resume_text=resume_text,
            github_username=github_username,
            linkedin_url=linkedin_url
        )
        
        # Generate session ID (simple hash for demo)
        import hashlib
        session_id = hashlib.md5(
            f"{resume_text}{github_username}{linkedin_url}".encode()
        ).hexdigest()[:8]
        
        # Store in session (in-memory)
        session_storage[session_id] = result
        
        # Redirect to result page
        return RedirectResponse(url=f"/result/{session_id}", status_code=303)
        
    except Exception as e:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "error": f"Internal server error: {str(e)}"
            }
        )


@app.post("/api/verify", response_model=VerifyResponse)
async def verify_credentials_api(request: VerifyRequest):
    """
    Verify user credentials using Gemini AI (API endpoint)
    
    Args:
        request: VerifyRequest with resume_text, github_username, linkedin_url
        
    Returns:
        VerifyResponse with trust_score, reasoning, and badge
    """
    try:
        # Validate input
        if not request.resume_text.strip():
            raise HTTPException(
                status_code=400,
                detail="Resume text is required"
            )
        
        if not request.github_username.strip():
            raise HTTPException(
                status_code=400,
                detail="GitHub username is required"
            )
        
        if not request.linkedin_url.strip():
            raise HTTPException(
                status_code=400,
                detail="LinkedIn URL is required"
            )
        
        # Call Gemini for analysis
        result = gemini_client.analyze_credentials(
            resume_text=request.resume_text,
            github_username=request.github_username,
            linkedin_url=request.linkedin_url
        )
        
        # Generate session ID (simple hash for demo)
        import hashlib
        session_id = hashlib.md5(
            f"{request.resume_text}{request.github_username}{request.linkedin_url}".encode()
        ).hexdigest()[:8]
        
        # Store in session (in-memory)
        session_storage[session_id] = result
        
        return VerifyResponse(
            trust_score=result["trust_score"],
            reasoning=result["reasoning"],
            badge=result["badge"],
            session_id=session_id
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/result/{session_id}")
async def get_result_api(session_id: str):
    """
    Retrieve verification result by session ID (API endpoint)
    
    Args:
        session_id: Session identifier
        
    Returns:
        Stored verification result
    """
    if session_id not in session_storage:
        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )
    
    result = session_storage[session_id]
    return VerifyResponse(
        trust_score=result["trust_score"],
        reasoning=result["reasoning"],
        badge=result["badge"],
        session_id=session_id
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

