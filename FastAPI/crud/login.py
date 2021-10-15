from sqlalchemy.orm import Session

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status as fastapi_status,
)
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.hash import sha256_crypt

import os
import sys
from pathlib import Path
sys.path.append(os.path.abspath(Path(os.getcwd()) / ".." ))
from database.database import get_db, engine
from models.user import User

import logging

####
# constants
# chave secreta da nossa aplicação que pode ser alterada de tempos em tempos
SECRET_KEY = "0a54f19e893f41f699d4a264e32300cc"
# tipo da cripto a ser utilizada
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 4320


class TokenData(BaseModel):
    username: Optional[str] = None

# crud part
async def retrieve_usernames(db: Session, username):
    """Função chamada pela rota post login, retorna o login de um user"""
    try:
        users = db.query(User.login).filter_by(login=username).one()
        return users#.fetchone()
    except Exception:
        logging.exception("ErrorRetrieveUsernames")
        return {}


async def retrieve_password(db: Session, username):
    """Função chamada pela rota post login, retorna a senha de um user"""
    try:
        users = db.query(User.password).filter_by(login=username).one()
        return users#.fetchall()[0].password
    except Exception:
        logging.exception("ErrorRetrievePassword")
        return {}


async def get_user_login(username: str, db: Session = Depends(get_db)):
    """tras os dados de login do banco e verifica se o usuario existe"""
    users = await retrieve_usernames(db, username)
    if username in users:
        return users


##############

# objetos criados para a estrutura de autenticassao

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
login_router = APIRouter()

##############
# UTILS
def verify_password(plain_password, hashed_password):
    """verifica se a senha inserida no login é válida para o usuario"""
    return sha256_crypt.verify(plain_password, hashed_password)


def get_password_hash(password):
    """criptografa a senha"""
    return sha256_crypt.hash(password)


# chamado pela rota de autentication
async def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
):
    """verifica se o usuario é valido"""
    user = await retrieve_usernames(db, username)
    if not user:
        return False
    if not verify_password(password, await retrieve_password(db, username)):
        return False
    return user


# codifica o token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """cria um token de acesso para permitir
    o uso de funções restritas por login"""

    # DATA contem o usuario  q esta logando
    to_encode = data.copy()
    # codifica o horario atual e etc para criar um token
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # encoded_jwt sao os dados de usuario e expire time juntos e  encriptados
    return encoded_jwt


# DEcodifica o token
# verifica qual eh o usuario q esta logando - serve para tratar casos onde determinado
# usuario n tem acesso a deerminado recurso
async def get_current_user_from_token(token: str = Depends(oauth2_scheme)):
    """verifica se o usuario logado é valido"""
    # caso o token seja invalido explode o except abaixo
    credentials_exception = HTTPException(
        status_code=fastapi_status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # decodifica o token - faz o oposto da function create_acess_token
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await get_user_login(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def retrieve_login_information(db: Session, user):
    try:
        data = db.query(User).filter_by(login=user).one()
    except:
        data = False
        logging.exception("ErrorGettingLoginData")
    finally:
      return data

