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
from crud.user import insert_user, get_user
from database.database import get_db
from PIL import Image
import cv2
from typing import List, Optional

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

@user_router.post("/user/preferences")
async def create_user_preferences(
    response: Response,
    user_id: int = Form(...),
    gm: int = Form(...),
    systems: str = Form(...),
    scenarios: str = Form(...),
    desc: str = Form(...),
    image: Optional[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    user = UserPreferencesPost
    user.user_id = user_id
    user.gm = gm
    user.systems = systems
    user.scenarios = scenarios
    user.desc = desc
    with open(Path(f"pictures/users/{user_id}.png"), "wb") as img:
        img.write(image.file.read())
    return insert_user_preferences(db, user)

@user_router.post("/user/relations")
async def create_user_relations(
    response: Response,
    user: UserRelationsPost,
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    return True
