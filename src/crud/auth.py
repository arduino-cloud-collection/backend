from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src import database
from src import settings
from src.crud import user as userCrud

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.config.JWT_KEY, algorithm=settings.config.ALGORITHM)
    return encoded_jwt


def decode_token(token):
    body = ""
    try:
        payload = jwt.decode(token, settings.config.JWT_KEY, algorithms=[settings.config.ALGORITHM])
        body: str = payload.get("user")
    except JWTError:
        body = False
    finally:
        return body


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = decode_token(token)
    if username:
        try:
            user = userCrud.get_user(db, username)
            return user
        except IntegrityError:
            raise HTTPException(status_code=403)
    else:
        raise HTTPException(status_code=403)
