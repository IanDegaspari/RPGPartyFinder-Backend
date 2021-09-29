from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class MsgPost(BaseModel):
    content: str
    by: int
    recipient_type: bool
    time: datetime

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "content": "andre@gmail.com",
                "by": 1,
                "recipient_type": True,
                "time": datetime.now()
            }
        }

class MsgToPost(BaseModel):
    msg_id: int
    to: int

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "msg_id": 1,
                "to": 1,
            }
        }