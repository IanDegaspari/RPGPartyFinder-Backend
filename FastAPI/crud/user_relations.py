import os
import sys
from pathlib import Path

from sqlalchemy.sql.elements import Null, or_, and_

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
        db.query(UserRelations).update({"swipe_0": -1})
        db.commit()
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

def update_user_relations(db: Session, user_relations: UserRelationsPost, user_id: int):
    try:
        if db.query(UserRelations).filter(or_(and_(UserRelations.user_1==user_relations.user_0,
                            UserRelations.user_0==user_relations.user_1), and_(UserRelations.user_1==user_relations.user_1,
                            UserRelations.user_0==user_relations.user_0))).first() is None:
            db_user = UserRelations(user_0 = user_relations.user_0, 
                                    user_1=user_relations.user_1, swipe_0= user_relations.swipe, swipe_1= -1)
            db.add(db_user)
            db.commit()
            potential_ally = -1
            status = True
        else:
            # print(user_relations.user_0 , "///" , user_relations.user_1)
            db.query(UserRelations).filter(UserRelations.user_0==user_relations.user_1,
                                              UserRelations.user_1==user_relations.user_0).update({"swipe_1": user_relations.swipe})
            db.commit()
            result = db.query(UserRelations).filter(UserRelations.user_1==user_relations.user_0,
                                                       UserRelations.user_0==user_relations.user_1).first()
            #print(result.swipe_1)
            ally = db.query(UserRelations).filter(or_(and_(UserRelations.user_1==user_relations.user_0,
                            UserRelations.user_0==user_relations.user_1), and_(UserRelations.user_1==user_relations.user_1,
                            UserRelations.user_0==user_relations.user_0))).first()
            potential_ally = ally.swipe_0
            status = True
    except Exception as ex:
        logging.exception(ex)
        status = False
        potential_ally = False        
    finally:
        # print(potential_ally)
        if potential_ally < 1:
            potential_ally = False
        else:
            potential_ally = True
        return {
            "potentialAlly": potential_ally,
            "status": status
        }

def delete_user_relations(db: Session, user_id_0: int, user_id_1: int):
    try:
        db.query(UserRelations).filter(or_(and_(UserRelations.user_0==user_id_0, UserRelations.user_1==user_id_1),
                                              and_(UserRelations.user_0==user_id_1, UserRelations.user_1==user_id_0))).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }