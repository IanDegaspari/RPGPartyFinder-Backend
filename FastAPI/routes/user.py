from fastapi import FastAPI, APIRouter, Depends, File
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Form
from starlette.responses import Response
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from crud.user_preferences import insert_user_preferences
from schemas.user import UserPost, UserPreferencesPost, UserRelationsPost
from crud.user import insert_user, get_user, update_user
from database.database import get_db
from PIL import Image
import cv2
from typing import List, Optional
from crud.login import oauth2_scheme

user_router = APIRouter()

@user_router.post("/user")
async def create_user(
    response: Response,
    user: UserPost,
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    return insert_user(db, user)

@user_router.get("/user/{id}")
async def get_users(id: int or None, response: Response, db: Session = Depends(get_db)):
    return get_user(db, id)

@user_router.put("/user")
async def put_user(user: UserPost, response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return update_user(db, user)

@user_router.delete("/user")
async def delete_user(id: int, response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return delete_user(db, id)
