import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from schemas.party import PartyPost
from models.party import Party, PartyUsers
from database.database import engine
from crud.party_users import get_party_users


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
        parties = []
        for party in results:
            party_dict = {"party_id": party.party_id, "name": party.name, "desc": party.desc, "allies": []}
            users = get_party_users(db, party.party_id)
            if users['status']:
                for usr in users['results']:
                    party_dict["allies"].append(usr.user_id)
                    if usr.role:
                        party_dict['admin'] = usr.user_id
            parties.append(party_dict)
        status = True
    except Exception:
        logging.exception("ErrorGettingData")
        status = False
    finally:
        return {
            "status": status, "results": parties
        }

def update_party(db: Session, party: PartyPost):
    try:
        db_party = Party(
            **party.dict())
        
        db.query(Party).filter(Party.party_id==db_party.party_id).update({"name": party.name, "desc": party.desc})
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
