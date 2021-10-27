from fastapi import (
    APIRouter,
    Form,
    Depends,
    HTTPException,
    status as fastapi_status,
    Response,
)
from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

import os
import sys
from pathlib import Path

sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from crud.user_preferences import get_user_preferences
from schemas.user import Login
from database.database import get_db
from crud import login, user_preferences
import io
from starlette.responses import StreamingResponse
import cv2
from robohash import Robohash

login_router = APIRouter()


@login_router.post("/token")
async def login_for_access_token(
    response: Response, inputdata: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """realiza o login do usuario"""
    data = ""
    # autentica
    user = await login.authenticate_user(inputdata.username, inputdata.password, db)
    # retorna erro
    if not user:
        response.status_code = fastapi_status.HTTP_401_UNAUTHORIZED
        return {
            "access_token": "",
            "token_type": "",
            "id": "",
            "login": "Invalid input",
            "name": "",
            "email": "",
            "preferences": {}
        }
    else:
        response.status_code = fastapi_status.HTTP_202_ACCEPTED
        # define o tempo de expirar o token
        access_token_expires = timedelta(minutes=login.ACCESS_TOKEN_EXPIRE_MINUTES)
        # criar um token baseado no tempo e no usuario
        # pega o role do banco
        access_token = login.create_access_token(
            data={"sub": user}, expires_delta=access_token_expires
        )
        data = await login.retrieve_login_information(db, user)
        # retorna o TOKEN gerado e um header falando q eh um bearer
        if data:
            preferences = {}
            results = user_preferences.get_user_preferences(db, data.id)
            if results['status'] and results['results'][0] is not None:
                preferences['gm'] = results['results'][0].gm
                preferences['systems'] = results['results'][0].systems
                preferences['scenarios'] = results['results'][0].scenarios
                preferences['desc'] = results['results'][0].desc
            token_data = {
                "access_token": access_token,
                "token_type": "bearer",
                "id": data.id,
                "login": user,
                "name": data.name,
                "email": data.email,
                "preferences": preferences
            }
        else:
            token_data = {
                "access_token": access_token,
                "token_type": "bearer",
                "id": "",
                "login": "",
                "name": "",
                "email": "",
                "preferences": {}
            }
    return token_data


@login_router.post("/token/json")
async def login_for_access_token(
    response: Response, inputdata: Login, db: Session = Depends(get_db)
):
    """realiza o login do usuario"""
    data = ""
    # autentica
    user = await login.authenticate_user(inputdata.login, inputdata.password, db)
    if not user:
        response.status_code = fastapi_status.HTTP_401_UNAUTHORIZED
        return {
            "access_token": "",
            "token_type": "",
            "id": "",
            "login": "Invalid input",
            "name": "",
            "email": "",
            "preferences": {}
        }
    else:
        response.status_code = fastapi_status.HTTP_202_ACCEPTED
        # define o tempo de expirar o token
        access_token_expires = timedelta(minutes=login.ACCESS_TOKEN_EXPIRE_MINUTES)
        # criar um token baseado no tempo e no usuario
        # pega o role do banco
        access_token = login.create_access_token(
            data={"sub": user}, expires_delta=access_token_expires
        )
        data = await login.retrieve_login_information(db, user)
        # retorna o TOKEN gerado e um header falando q eh um bearer
        if data:
            preferences = {}
            results = get_user_preferences(db, data.id)
            if results['status']:
                preferences['gm'] = results['results'][0].gm
                preferences['systems'] = results['results'][0].systems
                preferences['scenarios'] = results['results'][0].scenarios
                preferences['desc'] = results['results'][0].desc
            token_data = {
                "access_token": access_token,
                "token_type": "bearer",
                "id": data.id,
                "login": user,
                "name": data.name,
                "email": data.email,
                "preferences": preferences
            }
        else:
            token_data = {
                "access_token": access_token,
                "token_type": "bearer",
                "id": "",
                "login": "",
                "name": "",
                "email": "",
                "preferences": {}
            }
    return token_data

@login_router.get("/image/")
async def return_img(token: str = Depends(login.oauth2_scheme), db: Session = Depends(get_db)):
    lg = await login.get_current_user_from_token(token)
    user = await login.retrieve_login_information(db, lg)
    imgs_path = Path(f"pictures/user/{user.id}.png")
    if not os.path.isfile(imgs_path):
        rh = Robohash(str(user.id))
        rh.assemble(roboset="any")
        with open(imgs_path, 'wb') as f:
            rh.img.save(f, format="png")
    img = cv2.imread(str(imgs_path))
    res, im_png = cv2.imencode(".png", img)
    return StreamingResponse(io.BytesIO(im_png.tobytes()), media_type="image/png")