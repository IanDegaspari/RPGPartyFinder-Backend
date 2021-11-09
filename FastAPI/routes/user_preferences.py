from fastapi import FastAPI, APIRouter, Depends, File
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Form
from starlette.responses import Response
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from crud.user_preferences import insert_user_preferences, get_user_preferences, update_user_preferences, delete_user_preferences
from schemas.user import UserPost, UserPreferencesPost, UserRelationsPost
from database.database import get_db
from PIL import Image
import cv2
from typing import List, Optional
from crud.login import oauth2_scheme

pref_router = APIRouter()

@pref_router.post("/user/preferences")
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

@pref_router.get("/user/preferences/{id}")
async def get_prefs(id: int or None, response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_user_preferences(db, id)

@pref_router.put("/user/preferences")
async def put_prefs(user: UserPreferencesPost, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return update_user_preferences(db, user)

@pref_router.delete("/user/preferences")
async def delete_prefs(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return delete_user_preferences(db, id)