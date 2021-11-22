import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from schemas.party import PartyUsersPost, PartyUsersPut
from database.database import engine
from models.party import PartyUsers


def insert_party_users(db: Session, party_users: PartyUsersPost, id: int):
    try:
        db_party_users = PartyUsers(
            **party_users.dict(), party_id = id)
        db.add(db_party_users)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }
    
def insert_party_users(db: Session, party_users: PartyUsersPut):
    try:
        db_party_users = PartyUsers(
            **party_users.dict())
        db.add(db_party_users)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }

def get_party_users(db: Session, party_id: int or None):
    results = []
    try:
        if party_id is not None:
            results = db.query(PartyUsers).filter_by(party_id=party_id).all()
        else:
            results = db.query(PartyUsers).all()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_party_users(db: Session, party_users: PartyUsersPost):
    try:
        db_party_users = PartyUsers(
            **party_users.dict())
        
        db.query(PartyUsers).filter_by(party_id=db_party_users.party_id).update(db_party_users)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorUpdatingData")
        status = False
    finally:
        return {
            "status": status
        }

def delete_party_users(db: Session, party_id: int):
    try:
        db.query(PartyUsers).filter_by(party_id=party_id).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }
