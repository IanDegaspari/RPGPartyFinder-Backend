from datetime import date
from fastapi import FastAPI, APIRouter, Depends, File, status as fastapi_status
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Form
from sqlalchemy.sql.expression import true
from sqlalchemy.sql.functions import user
from starlette.responses import Response
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from crud.user_preferences import insert_user_preferences
from schemas.user import UserPost, UserPreferencesPost, UserRelationsPost
from crud.user import insert_user, get_user, update_user, delete_user, update_password, retrieve_cards
from database.database import get_db
from PIL import Image
import cv2
from typing import List, Optional
from crud.login import oauth2_scheme, get_current_user_from_token, retrieve_login_information

user_router = APIRouter()

@user_router.post("/user")
async def create_user(
    response: Response,
    user: UserPost,
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    data = insert_user(db, user)
    return data

@user_router.get("/user/{id}")
async def get_users(id: int or None, response: Response, db: Session = Depends(get_db)):
    return get_user(db, id)

@user_router.put("/user")
async def put_user(user: UserPost, response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return update_user(db, user)

@user_router.delete("/user")
async def dlt_user(id: int, response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return delete_user(db, id)

@user_router.put("/user/password")
async def put_password(password: str = Form(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    lg = await get_current_user_from_token(token)
    user = await retrieve_login_information(db, lg)
    return update_password(db, user.id, password)

@user_router.get("/cards")
async def get_cards(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    lg = await get_current_user_from_token(token)
    user = await retrieve_login_information(db, lg)
    return retrieve_cards(db, user.id)