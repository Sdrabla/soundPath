# main.py
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from auth import create_google_auth_url, exchange_code_for_token, get_user_info

from typing import List
import os

from managers.books_manager import BooksManager
from models.books_model import BookCreate, BookUpdate, BookOut

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

# Sessions needed for OAuth
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY", "supersecret"))

@app.get("/login")
async def login(request: Request):
    redirect_uri = "http://localhost:8000/auth"
    auth_url = create_google_auth_url(redirect_uri)
    return RedirectResponse(url=auth_url)

@app.get("/auth")
async def auth(request: Request):
    try:
        # Get the authorization code from the callback
        code = request.query_params.get("code")
        if not code:
            return RedirectResponse(url="http://localhost:5173/?error=no_code")
        
        redirect_uri = "http://localhost:8000/auth"
        
        # Exchange code for token
        token_data = await exchange_code_for_token(code, redirect_uri)
        access_token = token_data.get("access_token")
        
        if not access_token:
            return RedirectResponse(url="http://localhost:5173/?error=no_token")
        
        # Get user info
        user_info = await get_user_info(access_token)
        user_email = user_info.get("email", "")
        
        # Redirect back to frontend with user info
        return RedirectResponse(url=f"http://localhost:5173/?user={user_email}")
        
    except Exception as e:
        print(f"OAuth error: {e}")
        # Redirect to frontend with error
        return RedirectResponse(url=f"http://localhost:5173/?error=auth_failed")


# ---------- Manager ----------
books: BooksManager | None = None

@app.on_event("startup")
async def _startup():
    global books
    books = BooksManager(MONGO_URI, DB_NAME, COLLECTION)
    await books.connect()

@app.on_event("shutdown")
async def _shutdown():
    if books:
        await books.close()

# ---------- Routes ----------
@app.get("/ping")
async def ping():
    return {"message": "pong"}

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
