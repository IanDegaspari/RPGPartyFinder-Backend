from pydantic import BaseModel
from typing import Optional

class PartyPost(BaseModel):
    name: str
    desc: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "party do andre",
                "desc": "muito combate"
            }
        }

class PartyPut(BaseModel):
    id: int
    name: str
    desc: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "party do andre",
                "desc": "muito combate"
            }
        }

class PartyUsersPost(BaseModel):
    user_id: int
    role: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "user_id": 1,
                "role": True,
            }
        }

class PartyUsersWithId(BaseModel):
    party_id: int
    user_id: int
    role: bool

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "party_id": 1,
                "user_id": 1,
                "role": True,
            }
        }