import trafilatura
import requests
from urllib.parse import urlparse

def extract_from_url(url):
    """
    Extract job description from URL.
    Returns: (success: bool, text: str, error_message: str)
    """
    try:
        # Validate URL
        if not url.startswith(('http://', 'https://')):
            return False, "", "Invalid URL. Please include http:// or https://"
        
        # Fetch content
        downloaded = trafilatura.fetch_url(url)
        
        if not downloaded:
            return False, "", "Couldn't fetch the webpage. Check if URL is correct."
        
        # Extract main content
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True,
            no_fallback=False
        )
        
        if not text or len(text) < 100:
            return False, "", "Couldn't extract job description. Please try copy/paste instead."
        
        return True, text, ""
        
    except Exception as e:
        return False, "", f"Error: {str(e)}"

def validate_url(url):
    """Check if URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False