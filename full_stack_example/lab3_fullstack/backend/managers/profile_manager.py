from motor.motor_asyncio import AsyncIOMotorClient
from models.profile_model import ProfileCreate, ProfileOut
from bson import ObjectId

class ProfilesManager:
    def __init__(self, uri: str, db_name: str, collection: str):
        self.client = AsyncIOMotorClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection]

    async def connect(self):
        pass  # MongoDB client connects lazily

    async def close(self):
        self.client.close()

    async def create_profile(self, data: ProfileCreate) -> ProfileOut:
        doc = data.dict()
        result = await self.collection.insert_one(doc)
        return ProfileOut(id=str(result.inserted_id), **doc)

    async def list_profiles(self):
        cursor = self.collection.find()
        profiles = []
        async for doc in cursor:
            doc["id"] = str(doc["_id"])
            del doc["_id"]
            profiles.append(ProfileOut(**doc))
        return profiles

    async def get_profile(self, profile_id: str):
        doc = await self.collection.find_one({"_id": ObjectId(profile_id)})
        if not doc:
            return None
        doc["id"] = str(doc["_id"])
        del doc["_id"]
        return ProfileOut(**doc)
