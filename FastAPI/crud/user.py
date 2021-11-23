import os
import sys
from pathlib import Path

from sqlalchemy.sql.expression import and_, false, null, or_, true
from sqlalchemy.sql.functions import user

sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
import logging
import random
from sqlalchemy import exc
from sqlalchemy.orm import Session
from passlib.hash import sha256_crypt
from schemas.user import UserPost
from database.database import engine
from models.user import User, UserPreferences, UserRelations
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
        db_user = User(
            **user.dict())
        db_user.password = sha256_crypt.hash(db_user.password)
        db.add(db_user)
        db.commit()
        status = True
        id_temp = db.query(User.id).filter_by(login=user.login).first()
        id = id_temp.id
    except Exception:
        status = False
        logging.exception("ErrorInsertingData")
        if user.email in treatedEmails and user.login in treatedUsernames:
            error = 0
        elif user.email in treatedEmails:
            error = 1
        elif user.login in treatedUsernames:
            error = 2
    finally:
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
    password = sha256_crypt.hash(password)
    try:
        db.query(User).filter_by(id=user_id).update({'password': password})
        db.commit()
        status = True
    except:
        status = False
    return {"status": status}

def retrieve_cards(db: Session, user_id: int):
    retorno = []
    users_not_to_select = [user_id]
    try:
        not_slct = db.query(UserRelations).filter(or_(and_(UserRelations.user_0 == user_id, UserRelations.swipe_0 >= 0), and_(UserRelations.user_1 == user_id, UserRelations.swipe_1 >= 0))).all()
        for user in not_slct:
            #if user.user_0 not in users_not_to_select:
            users_not_to_select.append(user.user_0)
            #if user.user_1 not in users_not_to_select:
            users_not_to_select.append(user.user_1)
        cards = db.query(User, UserPreferences).filter(User.id == UserPreferences.user_id).filter(User.id.notin_(users_not_to_select)).all()
        for card in cards:
            retorno.append({
            "id": card.User.id,
            "name": card.User.name,
            "desc": card.UserPreferences.desc,
            "systems": card.UserPreferences.systems,
            "status": True
            })
    except Exception as ex:
        logging.exception(ex)
        retorno.append({
        "id": "",
        "name": "",
        "desc": '',
        "systems": [],
        "status": False
        })
    random.shuffle(retorno)
    return retorno

def retrieve_allies(db: Session, id: int):
    try:
        users_0 = db.query(UserRelations).filter(UserRelations.user_0==id, UserRelations.swipe_0 == 1, UserRelations.swipe_1 ==1).all()
        users_1 = db.query(UserRelations).filter(UserRelations.user_1==id, UserRelations.swipe_0 == 1, UserRelations.swipe_1 ==1).all()
        users = []
        for user in users_0:
            users.append(user.user_1)
        for user in users_1:
            users.append(user.user_0)
        allies = db.query(User, UserPreferences).filter(User.id == UserPreferences.user_id, User.id.in_(users)).all()
        status = True
        retorno = []
        for ally in allies:
            retorno.append({"id": ally.User.id, "name": ally.User.name, "desc": ally.UserPreferences.desc})
    except:
        logging.exception("ErrorGettingData")
        allies = []
        status = False
        retorno = []
        

    return {"allies": retorno, "status": status}