import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt
from schemas.user import UserPost
from database.database import engine
from models.user import User


def insert_user(db: Session, user: UserPost):
    try:
        db_user = User(
            **user.dict())
        db_user.password = sha256_crypt.hash(db_user.password)
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

def get_user(db: Session, user_id: int or None):
    results = []
    try:
        if user_id is not None:
            results = [db.query(User).filter_by(id=user_id).first()]
        else:
            results = db.query(User).all()
        status = True
    except Exception:
        logging.exception("ErrorGettingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_user(db: Session, user: UserPost):
    try:
        db_user = User(
            **user.dict())

        if db_user.password:
            db_user.password = sha256_crypt.hash(db_user.password)
        else:
            del db_user.password
        
        db.query(User).filter_by(id=db_user.id).update(db_user)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorUpdatingData")
        status = False
    finally:
        return {
            "status": status
        }

def delete_user(db: Session, user_id: int):
    try:
        db.query(User).filter_by(id=user_id).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }
