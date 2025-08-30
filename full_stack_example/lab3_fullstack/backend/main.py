# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from auth import create_google_auth_url, exchange_code_for_token, get_user_info

from typing import List
import os
from datetime import datetime

from managers.books_manager import BooksManager
from models.books_model import BookCreate, BookUpdate, BookOut
from managers.profile_manager import ProfilesManager
from models.profile_model import ProfileCreate, ProfileOut
from managers.user_manager import UserManager
from models.user_model import UserCreate, UserLogin, UserOut

app = FastAPI(title="Books API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Docker-friendly defaults; override via env
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.environ.get("MONGO_DB_NAME", "booksdb")
COLLECTION = os.environ.get("MONGO_COLLECTION", "books")

# Frontend URL for redirects
FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")

# Sessions needed for OAuth
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecret"))

# ---------- OAuth Routes ----------
@app.get("/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8000/auth"
    auth_url = create_google_auth_url(redirect_uri)
    return RedirectResponse(url=auth_url)

@app.get("/auth")
async def auth(request: Request):
    try:
        # Check for error parameter first
        error = request.query_params.get("error")
        if error:
            error_description = request.query_params.get("error_description", "OAuth error")
            return RedirectResponse(url=f"{FRONTEND_URL}/?error={error}&description={error_description}")
        
        # Get the authorization code from the callback
        code = request.query_params.get("code")
        if not code:
            return RedirectResponse(url=f"{FRONTEND_URL}/?error=no_code&description=No authorization code received")
        
        redirect_uri = "http://localhost:8000/auth"
        
        # Exchange code for token
        try:
            token_data = await exchange_code_for_token(code, redirect_uri)
            access_token = token_data.get("access_token")
            
            if not access_token:
                return RedirectResponse(url=f"{FRONTEND_URL}/?error=no_token&description=No access token received")
        except Exception as token_error:
            print(f"OAuth token error: {token_error}")
            return RedirectResponse(url=f"{FRONTEND_URL}/?error=token_error&description=Token exchange failed")
        
        # Get user info
        try:
            user_info = await get_user_info(access_token)
            user_email = user_info.get("email", "")
            
            if not user_email:
                return RedirectResponse(url=f"{FRONTEND_URL}/?error=no_email&description=No email received")
            
            # Check if user exists, if not create them
            assert users is not None
            existing_user = await users.collection.find_one({"email": user_email})
            
            if not existing_user:
                # Create new user from Google OAuth
                now = datetime.utcnow()
                user_doc = {
                    "email": user_email,
                    "name": f"{user_info.get('given_name', 'Google')} {user_info.get('family_name', 'User')}",
                    "password_hash": "",  # OAuth users don't have passwords
                    "created_at": now,
                    "updated_at": now
                }
                
                result = await users.collection.insert_one(user_doc)
                user_doc["id"] = str(result.inserted_id)
                user = UserOut(**user_doc)
            else:
                # User exists, convert to UserOut format
                existing_user["id"] = str(existing_user["_id"])
                del existing_user["_id"]
                del existing_user["password_hash"]
                user = UserOut(**existing_user)
            
            # Create token
            token = users.create_token(user.id, user.email)
            
            # Redirect back to frontend with user info and token
            return RedirectResponse(url=f"{FRONTEND_URL}/?token={token}&user={user_email}")
            
        except Exception as user_info_error:
            print(f"OAuth user info error: {user_info_error}")
            return RedirectResponse(url=f"{FRONTEND_URL}/?error=user_info_error&description=Failed to get user info")
        
    except Exception as e:
        print(f"OAuth error: {e}")
        return RedirectResponse(url=f"{FRONTEND_URL}/?error=unexpected&description=Unexpected error")


# ---------- Managers ----------
books: BooksManager | None = None
profiles: ProfilesManager | None = None
users: UserManager | None = None

@app.on_event("startup")
async def startup_event():
    global books, profiles, users
    
    # Books manager
    books = BooksManager(MONGO_URI, DB_NAME, COLLECTION)
    await books.connect()
    
    # Profiles manager
    profiles = ProfilesManager(MONGO_URI, "musicdb", "profiles")
    await profiles.connect()
    
    # Users manager
    users = UserManager(MONGO_URI, "musicdb", "users")
    await users.connect()

@app.on_event("shutdown")
async def shutdown_event():
    if books:
        await books.close()
    if profiles:
        await profiles.close()
    if users:
        await users.close()

# ---------- Health Check ----------
@app.get("/ping")
async def ping():
    return {"message": "pong"}

# ---------- Books Routes ----------
@app.get("/books", response_model=List[BookOut], response_model_exclude_none=True)
async def list_books():
    assert books is not None
    return await books.list_books()

@app.get("/books/{book_id}", response_model=BookOut, response_model_exclude_none=True)
async def get_book(book_id: str):
    assert books is not None
    found = await books.get_book(book_id)
    if not found:
        raise HTTPException(status_code=404, detail="Book not found")
    return found

@app.post("/books", response_model=BookOut, status_code=201, response_model_exclude_none=True)
async def create_book(data: BookCreate):
    """
    Pass the Pydantic model through; manager can call model_dump()/dict().
    """
    assert books is not None
    return await books.create_book(data)

@app.put("/books/{book_id}", response_model=BookOut, response_model_exclude_none=True)
async def update_book(book_id: str, data: BookUpdate):
    assert books is not None
    payload = data.model_dump(exclude_none=True)
    if not payload:
        raise HTTPException(status_code=400, detail="No fields to update")
    updated = await books.update_book(book_id, payload)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.delete("/books/{book_id}", status_code=204)
async def delete_book(book_id: str):
    assert books is not None
    ok = await books.delete_book(book_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Book not found")

# ---------- Profile Routes ----------
@app.post("/profiles", response_model=ProfileOut, status_code=201)
async def create_profile(data: ProfileCreate):
    assert profiles is not None
    return await profiles.create_profile(data)

@app.get("/profiles", response_model=List[ProfileOut])
async def list_profiles():
    assert profiles is not None
    return await profiles.list_profiles()

# ---------- User Routes ----------
@app.post("/api/register", response_model=UserOut, status_code=201)
async def register_user(data: UserCreate):
    """Register a new user"""
    assert users is not None
    try:
        user = await users.register_user(data)
        # Create token for the new user
        token = users.create_token(user.id, user.email)
        return {
            "success": True,
            "message": "User registered successfully",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/api/login")
async def login_user(data: UserLogin):
    """Login a user"""
    assert users is not None
    try:
        user, token = await users.authenticate_user(data)
        return {
            "success": True,
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")