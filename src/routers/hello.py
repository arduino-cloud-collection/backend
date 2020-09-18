from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from pydantic import BaseModel
from src.crud import auth as authCrud
from src.crud import user as userCrud
from src.models import user as userModel
from src import database
from sqlalchemy.orm import Session
from jose import jwt
from src import settings


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")



class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


def fake_decode_token(token):
    payload = jwt.decode(token, settings.config.JWT_KEY, algorithms=[settings.config.ALGORITHM])
    body: str = payload.get("user")
    return body


async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    username = fake_decode_token(token)
    user = userCrud.get_user(db, username)
    return user


@router.get("/")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
