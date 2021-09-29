from pydantic import BaseModel, EmailStr
from typing import Optional

class UserPost(BaseModel):
    email: EmailStr
    name: str
    password: str
    login: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "andre@gmail.com",
                "name": "andre",
                "password": "carlosgostoso",
                "login": "andresrib"
            }
        }

class UserPreferencesPost(BaseModel):
    user_id: int
    gm: bool
    systems: str
    scenarios: str
    desc: str
    
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": 1,
                "gm": True,
                "systems": "Tormenta",
                "scenarios": "Medieval",
                "desc": "Nerdola"
            }
        }

class UserRelationsPost(BaseModel):
    user_0: int
    user_1: int
    swipe_0: bool
    swipe_1: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_0": 1,
                "user_1": 2,
                "swipe_0": False,
                "swipe_1": False
            }
        }