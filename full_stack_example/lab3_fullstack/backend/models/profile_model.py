
from pydantic import BaseModel
from typing import List

class ProfileCreate(BaseModel):
    user_id: str
    name: str
    experience: str
    instrument: str
    goal: str
    genres: List[str]
    gear: List[str]  

class ProfileOut(ProfileCreate):
    pass  