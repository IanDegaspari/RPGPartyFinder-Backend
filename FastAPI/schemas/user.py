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
                "email": "jack@gmail.com",
                "cpf": "12345678901",
                "name": "jack",
                "password": "jack",
                "role": "customer",
                "city": "Piracicaba",
                "state": "SP",
                "telephone": "40543039",
            }
        }