import os
from dotenv import load_dotenv
import google.generativeai as genai

def load_and_configure_api():
    """Load environment variables and configure Google API key."""
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment variables.")
    genai.configure(api_key=api_key)
    return api_key
