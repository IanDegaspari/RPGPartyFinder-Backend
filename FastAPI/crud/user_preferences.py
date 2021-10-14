from sqlalchemy.orm import Session
import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from schemas.user import UserPreferencesPost
from database.database import engine
from models.user import UserPreferences

def insert_user_preferences(db: Session, user_pref: UserPreferencesPost):
    try:
        db_userp = UserPreferences(
            **user_pref.dict())
        db.add(db_userp)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }

def get_user_preferences(db: Session, user_id: int or None):
    results = []
    try:
        if user_id is not None:
            results = [db.query(UserPreferences).filter_by(user_id=user_id).first()]
        else:
            results = db.query(UserPreferences).all()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_user_preferences(db: Session, user_pref: UserPreferencesPost):
    try:
        db_userp = UserPreferences(
            **user_pref.dict())

        db.query(UserPreferences).filter_by(user_id=db_userp['user_id']).update(db_userp)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }

def delete_user_preferences(db: Session, user_id: int):
    try:
        db.query(UserPreferences).filter_by(user_id=user_id).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }