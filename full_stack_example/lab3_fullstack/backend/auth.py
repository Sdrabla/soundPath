import os
import httpx
from urllib.parse import urlencode

# Store OAuth credentials
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

# OAuth scopes
GOOGLE_SCOPES = ["openid", "email", "profile"]

def create_google_auth_url(redirect_uri, state=None):
    """Create Google OAuth authorization URL"""
    
    # Validate that we have the client ID
    if not GOOGLE_CLIENT_ID:
        raise ValueError("GOOGLE_CLIENT_ID environment variable not set")
    
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(GOOGLE_SCOPES),
        'response_type': 'code',
        'access_type': 'offline',
        'include_granted_scopes': 'true'
    }
    
    if state:
        params['state'] = state
    
    url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    print(f"Generated OAuth URL: {url}")  # Debug logging
    return url

async def exchange_code_for_token(code, redirect_uri):
    """Exchange authorization code for access token"""
    
    if not GOOGLE_CLIENT_ID or not GOOGLE_CLIENT_SECRET:
        raise ValueError("Google OAuth credentials not properly configured")
    
    async with httpx.AsyncClient() as client:
        data = {
            'client_id': GOOGLE_CLIENT_ID,
            'client_secret': GOOGLE_CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': redirect_uri
        }
        
        try:
            response = await client.post(GOOGLE_TOKEN_URL, data=data)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"Token exchange error: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response content: {e.response.text}")
            raise

async def get_user_info(access_token):
    """Get user information from Google"""
    async with httpx.AsyncClient() as client:
        headers = {'Authorization': f'Bearer {access_token}'}
        
        try:
            response = await client.get(GOOGLE_USERINFO_URL, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            print(f"User info error: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response content: {e.response.text}")
            raise