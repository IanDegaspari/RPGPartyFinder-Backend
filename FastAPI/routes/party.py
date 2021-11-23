from fastapi import FastAPI, APIRouter, Depends, File
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Form
from pydantic.utils import almost_equal_floats
from starlette.responses import Response
import os
import sys
from pathlib import Path
from typing import List
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from crud.user_relations import insert_user_relations, update_user_relations, get_user_relations, delete_user_relations
from schemas.party import PartyPost, PartyPut, PartyUsersPost, PartyUsersWithId
from crud.party_users import insert_party_users, insert_party_user
from crud.party import insert_party, retrieve_party, update_party, delete_party
from database.database import get_db
from crud.login import oauth2_scheme, get_current_user_from_token, retrieve_login_information

party_router = APIRouter()

@party_router.post("/party")
async def create_party(party: PartyPost, users: List[PartyUsersPost], db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    party_return = insert_party(db, party)
    status_users = []
    for user in users:
        status_users.append(insert_party_users(db, user, party_return["id"]))
    return {"status_party": party_return["status"], "status_users": status_users, "party_id": party_return["id"]}

@party_router.get("/party")
async def get_party(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    lg = await get_current_user_from_token(token)
    user = await retrieve_login_information(db, lg)
    return retrieve_party(db, user.id)

@party_router.put("/party/{id}")
async def put_party(id: int, party: PartyPut, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return update_party(db, party)

@party_router.delete("party/{id}")
async def dlt_party(id: int, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return delete_party(db, id)

@party_router.post("/add/ally")
async def post_ally(ally: PartyUsersWithId, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    return insert_party_user(db, ally)

@party_router.post("/party/image")
async def put_image(id: int = Form(...), image: UploadFile = File(...), token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        with open(Path(f"pictures/party/{id}.png"), "wb") as img:
            img.write(image.file.read())
            status = True
    except:
        status = False
    return {"status": status}