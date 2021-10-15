import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy.orm import Session
from schemas.msg import MsgPost
from database.database import engine
from models.msg import Msg


def insert_msg(db: Session, msg: MsgPost):
    try:
        db_msg = Msg(
            **msg.dict())
        db.add(db_msg)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorInsertingData")
        status = False
    finally:
        return {
            "status": status
        }

def get_msg(db: Session, msg_id: int or None, by: int or None):
    results = []
    try:
        if msg_id is not None:
            results = [db.query(Msg).filter_by(msg_id=msg_id).first()]
        elif by is not None:
            results = db.query(Msg).filter_by(by=by).all()
        else:
            results = db.query(Msg).all()
        status = True
    except Exception:
        logging.exception("ErrorGettingData")
        status = False
    finally:
        return {
            "status": status, "results": results
        }

def update_msg(db: Session, msg: MsgPost):
    try:
        db_msg = Msg(
            **msg.dict())
        
        db.query(Msg).filter_by(msg_id=db_msg.msg_id).update(db_msg)
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorUpdatingData")
        status = False
    finally:
        return {
            "status": status
        }

def delete_msg(db: Session, msg_id: int):
    try:
        db.query(Msg).filter_by(msg_id=msg_id).delete()
        db.commit()
        status = True
    except Exception:
        logging.exception("ErrorDeletingData")
        status = False
    finally:
        return {
            "status": status
        }
