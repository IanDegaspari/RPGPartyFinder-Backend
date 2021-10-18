from fastapi import FastAPI, APIRouter, Depends
from starlette.responses import Response
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from crud.user_preferences import insert_user_preferences
from schemas.user import UserPost, UserPreferencesPost, UserRelationsPost
from crud.user import insert_user
from database.database import get_db

user_router = APIRouter()

@user_router.post("/user")
async def create_user(
    response: Response,
    user: UserPost,
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    return insert_user(db, user)


@user_router.post("/user/preferences")
async def create_user_preferences(
    response: Response,
    user: UserPreferencesPost,
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    return insert_user_preferences(db, user)

@user_router.post("/user/relations")
async def create_user_relations(
    response: Response,
    user: UserRelationsPost,
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    return True