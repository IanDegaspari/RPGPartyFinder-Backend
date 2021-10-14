from uuid import uuid4
from sqlalchemy.orm import Session
import sqlalchemy


import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from schemas.user import UserPost
from database.database import engine
from models.user import UserModel
import logging


def insert_user(db: Session, user: UserPost):
    status = False
    try:
        db_user = UserModel(
            **user.dict())
        
        db.add(db_user)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }