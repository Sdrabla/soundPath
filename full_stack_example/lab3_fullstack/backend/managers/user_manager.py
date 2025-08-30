from motor.motor_asyncio import AsyncIOMotorClient
from models.user_model import UserCreate, UserLogin, UserOut, UserInDB
from bson import ObjectId
from datetime import datetime
import bcrypt
import jwt
import os
from typing import Optional

class UserManager:
    def __init__(self, uri: str, db_name: str, collection: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection]
        self.secret_key = os.getenv("SECRET_KEY", "supersecret")

    async def connect(self):
        pass  # MongoDB client connects lazily

    async def close(self):
        self.client.close()

    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def create_token(self, user_id: str, email: str) -> str:
        """Create a JWT token for the user"""
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": datetime.utcnow() + datetime.timedelta(days=7)  # 7 days expiry
        }
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    async def register_user(self, user_data: UserCreate) -> UserOut:
        """Register a new user"""
        # Check if user already exists
        existing_user = await self.collection.find_one({"email": user_data.email})
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash the password
        password_hash = self.hash_password(user_data.password)
        
        # Create user document
        now = datetime.utcnow()
        user_doc = {
            "email": user_data.email,
            "password_hash": password_hash,
            "name": user_data.name,
            "created_at": now,
            "updated_at": now
        }
        
        result = await self.collection.insert_one(user_doc)
        user_doc["id"] = str(result.inserted_id)
        
        return UserOut(**user_doc)

    async def authenticate_user(self, login_data: UserLogin) -> tuple[UserOut, str]:
        """Authenticate a user and return user data with token"""
        # Find user by email
        user_doc = await self.collection.find_one({"email": login_data.email})
        if not user_doc:
            raise ValueError("Invalid email or password")
        
        # Verify password
        if not self.verify_password(login_data.password, user_doc["password_hash"]):
            raise ValueError("Invalid email or password")
        
        # Create token
        token = self.create_token(str(user_doc["_id"]), user_doc["email"])
        
        # Return user data (without password hash)
        user_doc["id"] = str(user_doc["_id"])
        del user_doc["_id"]
        del user_doc["password_hash"]
        
        return UserOut(**user_doc), token

    async def get_user_by_id(self, user_id: str) -> Optional[UserOut]:
        """Get user by ID"""
        user_doc = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user_doc:
            return None
        
        user_doc["id"] = str(user_doc["_id"])
        del user_doc["_id"]
        del user_doc["password_hash"]
        
        return UserOut(**user_doc)
