import os
import sys
from pathlib import Path

from sqlalchemy.sql.expression import desc, true
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from schemas.user import UserPreferencesPost
from database.database import engine
from models.user import UserPreferences

def insert_user_preferences(db: Session, user_pref: UserPreferencesPost):
    try:
        if user_pref.systems == "|":
            user_pref.systems = ""
        if user_pref.scenarios == "|":
            user_pref.scenarios = ""
        db_userp = UserPreferences(
            user_id=user_pref.user_id, gm=user_pref.gm, desc=user_pref.desc, scenarios=user_pref.scenarios, systems=user_pref.systems)
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
        logging.exception("ErrorGettingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_user_preferences(db: Session, user_pref: UserPreferencesPost):
    try:
        db.query(UserPreferences).filter_by(user_id=user_pref.user_id).update({'desc': user_pref.desc, 'gm': user_pref.gm, 'systems': user_pref.systems, 'scenarios': user_pref.scenarios})
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorUpdatingData")
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
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }