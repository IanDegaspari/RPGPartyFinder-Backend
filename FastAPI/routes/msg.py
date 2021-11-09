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
from schemas.msg import MsgPost
from database.database import get_db
from PIL import Image
import cv2
from typing import List, Optional
from crud.login import oauth2_scheme

msg_router = APIRouter()
