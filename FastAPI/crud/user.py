import os
import sys
from pathlib import Path

from sqlalchemy.sql.expression import false, true

sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
from sqlalchemy import exc
from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt
from schemas.user import UserPost
from database.database import engine
from models.user import User
import logging

def insert_user(db: Session, user: UserPost):
    id = ""
    error = ""
    status = ""
    usernames = db.query(User.login).all()
    treatedUsernames = []
    treatedEmails = []
    for username in usernames:
        treatedUsernames.append(username[0])
    emails = db.query(User.email).all()
    for email in emails:
        treatedEmails.append(email[0])
    try:
        print("a")
        db_user = User(
            **user.dict())
        db_user.password = sha256_crypt.hash(db_user.password)
        db.add(db_user)
        db.commit()
        print("b")
        status = True
        print("c")
        id_temp = db.query(User.id).filter_by(login=user.login).first()
        id = id_temp.id
    except Exception:
        status = False
        logging.exception("ErrorInsertingData")
        if user.email in treatedEmails and user.login in treatedUsernames:
            print(0)
            error = 0
        elif user.email in treatedEmails:
            print(1)
            error = 1
        elif user.login in treatedUsernames:
            print(2)
            error = 2
    finally:
        print(id)
        return {
            "status": status,
            "id": id,
            "error": error
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
        
        old_user_passw = db.query(User.password).filter_by(id=db_user.id).first()
        db_user.password = old_user_passw
        
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

def update_password(db: Session, user_id: int, password: str):
    print(password)
    password = sha256_crypt.hash(password)
    print(password)
    try:
        db.query(User).filter_by(id=user_id).update({'password': password})
        db.commit()
        status = true
    except:
        status = false
    return {"status": status}