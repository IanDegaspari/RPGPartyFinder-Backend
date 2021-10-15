import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from schemas.msg import MsgToPost
from database.database import engine
from models.msg import MsgTo


def insert_msg_to(db: Session, msg_to: MsgToPost):
    try:
        db_msg_to = MsgTo(
            **msg_to.dict())
        db.add(db_msg_to)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }

def get_msg_to(db: Session, msg_id: int or None, to: int or None):
    results = []
    try:
        if msg_id is not None:
            results = [db.query(MsgTo).filter_by(msg_id=msg_id).first()]
        elif to is not None:
            results = db.query(MsgTo).filter_by(to=to).all()
        else:
            results = db.query(MsgTo).all()
        status = True
    except Exception:
        logging.exception("ErrorGettingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_msg_to(db: Session, msg_to: MsgToPost):
    try:
        db_msg_to = MsgTo(
            **msg_to.dict())
        
        db.query(MsgTo).filter_by(msg_id=db_msg_to['msg_id']).update(db_msg_to)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorUpdatingData")
        status = False
    finally:
        return {
            "status": status
        }

def delete_msg_to(db: Session, msg_id: int):
    try:
        db.query(MsgTo).filter_by(msg_id=msg_id).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }
