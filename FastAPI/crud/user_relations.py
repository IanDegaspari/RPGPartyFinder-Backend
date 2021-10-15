import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from schemas.user import UserRelationsPost
from database.database import engine
from models.user import UserRelations

def insert_user_relations(db: Session, user_relations: UserRelationsPost):
    try:
        db_userr = UserRelations(
            **user_relations.dict())
        db.add(db_userr)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }

def get_user_relations(db: Session, user_id_0: int or None, user_id_1: int or None):
    results = []
    try:
        if user_id_0 is None:
            results = db.query(UserRelations).all()
        elif user_id_0 is not None and user_id_1 is None:
            results = db.query(UserRelations).filter_by(user_0=user_id_0).all()
        else:
            results = [db.query(UserRelations).filter_by(user_0=user_id_0, user_1=user_id_1).first()]
        status = True
    except Exception:
        logging.exception("ErrorGettingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_user_relations(db: Session, user_relations: UserRelationsPost):
    try:
        db_userr = UserRelations(
            **user_relations.dict())

        db.query(UserRelations).filter_by(user_0=db_userr['user_0'], user_1=db_userr['user_1']).update(db_userr)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorUpdatingData")
        status = False
    finally:
        return {
            "status": status
        }

def delete_user_relations(db: Session, user_id_0: int, user_id_1: int):
    try:
        db.query(UserRelations).filter_by(user_0=user_id_0, user_1=user_id_1).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }