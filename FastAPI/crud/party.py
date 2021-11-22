import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from schemas.party import PartyPost
from models.party import Party
from database.database import engine
from models.party import Party


def insert_party(db: Session, party: PartyPost):
    try:
        db_party = Party(
            **party.dict())
        db.add(db_party)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status, "id": db_party.party_id
        }

def retrieve_party(db: Session, party_id: int or None):
    results = []
    try:
        if party_id is not None:
            results = [db.query(Party).filter_by(party_id=party_id).first()]
        else:
            results = db.query(Party).all()
        status = True
    except Exception:
        logging.exception("ErrorGettingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_party(db: Session, party: PartyPost):
    try:
        db_party = Party(
            **party.dict())
        
        db.query(Party).filter_by(party_id=db_party.party_id).update(db_party)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorUpdatingData")
        status = False
    finally:
        return {
            "status": status
        }

def delete_party(db: Session, party_id: int):
    try:
        db.query(Party).filter_by(party_id=party_id).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }
