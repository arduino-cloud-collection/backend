from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from arduino_backend.database import get_db
from arduino_backend.user.models import User
from arduino_backend.token.models import Token
from arduino_backend.token.schemas import token_schema, token_return_schema, token_update_schema

router = APIRouter()


@router.get("/", tags=["token"])
def get_tokens(db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    tokens = Token.all(db, current_user)
    tokens_schema = token_return_schema.list_parse(tokens)
    return tokens_schema


@router.post("/", tags=["token"])
def add_token(data: token_schema, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    new_token = Token.create(db, data, current_user)
    return_schema = token_return_schema.from_orm(new_token)
    return return_schema


@router.get("/{token_id}", tags=["token"])
def get_single_token(token_id: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    token = Token.by_name(db, token_id)
    if token.owner == current_user:
        return token
    else:
        HTTPException(403)


@router.delete("/{token_id}", tags=["token"])
def edit_token(token_id: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    token = Token.by_name(db, token_id)
    if token.owner == current_user:
        return token.delete(db)
    else:
        HTTPException(403)


@router.put("/{token_id}", tags=["token"])
def delete_token(token_id: str, update_data: token_update_schema ,db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    token = Token.by_name(db, token_id)
    if token.owner == current_user:
        return token.update(db, update_data)
    else:
        HTTPException(403)
