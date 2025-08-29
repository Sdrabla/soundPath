# main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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


#user_profiling
from managers.profile_manager import ProfilesManager
from models.profile_model import ProfileCreate, ProfileOut

MONGO_URI = "mongodb://127.0.0.1:27017"  # local MongoDB
DB_NAME = "musicdb"                       # name of your database

@app.get("/ping")
async def ping():
    return {"message": "pong"}

profiles: ProfilesManager | None = None

@app.on_event("startup")
async def startup_profiles():
    global profiles
    profiles = ProfilesManager(MONGO_URI, DB_NAME, "profiles")
    await profiles.connect()

@app.on_event("shutdown")
async def shutdown_profiles():
    if profiles:
        await profiles.close()

@app.post("/profiles", response_model=ProfileOut, status_code=201)
async def create_profile(data: ProfileCreate):
    assert profiles is not None
    return await profiles.create_profile(data)

from typing import List

@app.get("/profiles", response_model=List[ProfileOut])
async def list_profiles():
    assert profiles is not None
    return await profiles.list_profiles()



