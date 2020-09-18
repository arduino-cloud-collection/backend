from fastapi import Depends, HTTPException, status
from datetime import datetime, timedelta
from src import settings
from src.crud import user as userCrud
from src.models import user as userModel
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src import database

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


def get_current_user(token: str = Depends(oauth2_scheme)):
    db = database.get_db()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.config.JWT_KEY, algorithms=[settings.config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return False
        token_data = username
    except:
        return False
    user = userCrud.get_user(db, username=token_data.username)
    if user is None:
        raise False
    return user

