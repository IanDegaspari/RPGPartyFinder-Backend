from fastapi import FastAPI, APIRouter, Depends, File
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Form
from starlette.responses import Response
import os
import sys
from pathlib import Path
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from crud.user_relations import insert_user_relations, update_user_relations, get_user_relations, delete_user_relations
from schemas.user import UserPost, UserPreferencesPost, UserRelationsPost
from database.database import get_db
from crud.login import oauth2_scheme, get_current_user_from_token, retrieve_login_information

relations_router = APIRouter()

@relations_router.post("/user/relations")
async def create_user_relations(
    response: Response,
    user: UserRelationsPost,
    db: Session = Depends(get_db)
):
    #chamar função que salva o usuário no banco e retornar true ou false
    return True

@relations_router.get("/user/relations/{id0}/{id1}")
async def get_rel(response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return get_user_relations(db, None, None)

@relations_router.put("/user/relations")
async def put_rel(relation: UserRelationsPost, response: Response, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    lg = await get_current_user_from_token(token)
    user = await retrieve_login_information(db, lg)
    return update_user_relations(db, relation, user.id)

@relations_router.delete("/user/relations")
async def delete_rel(id0, id1, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return delete_user_relations(db, id0, id1) 

