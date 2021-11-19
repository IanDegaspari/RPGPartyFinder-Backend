from fastapi import FastAPI, APIRouter, Depends, File
from fastapi.datastructures import UploadFile
from fastapi.param_functions import Form
from pydantic.utils import almost_equal_floats
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

party_router = APIRouter()

@party_router.post("/party")
async def create_party():
    pass