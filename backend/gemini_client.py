"""
Gemini Client for CredibleMe
Handles integration with Google Gemini 1.5 Flash API
"""
import os
import google.generativeai as genai
from typing import Optional, Dict, Any


class GeminiClient:
    """Client for interacting with Gemini 1.5 Flash API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client
        
        Args:
            api_key: Google AI Studio API key. If None, uses mock mode.
        """
        # Resolve API key from argument or environment variable. Do not fall
        # back to a mock response — require a valid key so failures are
        # visible instead of silently returning fake data.
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        if not self.api_key:
            raise RuntimeError(
                "GEMINI_API_KEY not set. Please set the GEMINI_API_KEY environment variable or pass api_key to GeminiClient."
            )

        # Initialize the real Gemini model. Raise on failure so callers can
        # handle the error explicitly.
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash')
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Gemini API: {e}")
    
    def analyze_credentials(
        self,
        resume_text: str,
        github_username: str,
        linkedin_url: str
    ) -> Dict[str, Any]:
        """
        Analyze user credentials for consistency and trustworthiness
        
        Args:
            resume_text: Text content from resume
            github_username: GitHub username
            linkedin_url: LinkedIn profile URL
            
        Returns:
            Dictionary with trust_score, reasoning, and badge
        """
        # Build the prompt and call the real Gemini model. Any exception is
        # raised to the caller so the backend surfaces the failure (HTTP 500)
        # instead of returning synthetic/mock data.
        prompt = self._build_analysis_prompt(
            resume_text, github_username, linkedin_url
        )

        try:
            response = self.model.generate_content(prompt)
        except Exception as e:
            raise RuntimeError(f"Error calling Gemini API: {e}")

        # Parse Gemini response
        return self._parse_response(response.text)
    
    def _build_analysis_prompt(
        self,
        resume_text: str,
        github_username: str,
        linkedin_url: str
    ) -> str:
        """Build the prompt for Gemini analysis"""
        # Limit resume text to first 2000 characters
        resume_content = resume_text[:2000] if len(resume_text) > 2000 else resume_text
        
        return f"""
You are an expert credential verification analyst. Analyze the following digital credentials for consistency and trustworthiness.

RESUME CONTENT:
{resume_content}

GITHUB USERNAME:
{github_username}

LINKEDIN URL:
{linkedin_url}

Please analyze:
1. Consistency between resume claims and GitHub/LinkedIn profiles
2. Credibility indicators (activity, completeness, alignment)
3. Potential red flags or inconsistencies

Provide your analysis in the following JSON format:
{{
    "trust_score": <number between 0-100>,
    "reasoning": "<detailed explanation of your analysis>",
    "badge": "<Verified|Needs Review|Unverified>"
}}

Focus on:
- Matching skills/projects between resume and GitHub
- Professional experience alignment with LinkedIn
- Overall credibility and consistency
"""
    
    def _parse_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini response into structured format"""
        try:
            # Try to extract JSON from response
            import json
            import re
            
            # Look for JSON in the response
            json_match = re.search(r'\{[^{}]*"trust_score"[^{}]*\}', response_text, re.DOTALL)
            if json_match:
                parsed = json.loads(json_match.group())
                return {
                    "trust_score": int(parsed.get("trust_score", 75)),
                    "reasoning": parsed.get("reasoning", "Analysis completed"),
                    "badge": parsed.get("badge", "Verified")
                }
        except Exception as e:
            print(f"Error parsing response: {e}")
        
        # Fallback: extract score and reasoning from text
        score_match = re.search(r'trust_score["\s:]+(\d+)', response_text)
        score = int(score_match.group(1)) if score_match else 75
        
        return {
            "trust_score": score,
            "reasoning": response_text[:500] if response_text else "Analysis completed",
            "badge": "Verified" if score >= 70 else "Needs Review"
        }
    
    # Note: mock fallback intentionally removed. If you need offline testing,
    # add a separate mock client or wrap this class in a test double.

