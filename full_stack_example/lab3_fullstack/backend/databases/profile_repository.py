from pymongo import MongoClient

class ProfileRepository:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")  # change if needed
        self.db = self.client["soundpath"]
        self.collection = self.db["profiles"]

    def save_profile(self, profile_dict):
        existing = self.collection.find_one({"user_id": profile_dict["user_id"]})
        if existing:
            self.collection.update_one({"user_id": profile_dict["user_id"]}, {"$set": profile_dict})
        else:
            self.collection.insert_one(profile_dict)
        return profile_dict
