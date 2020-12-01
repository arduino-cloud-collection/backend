from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from arduino_backend.database import get_db
from arduino_backend.user.models import User
from arduino_backend.token.models import Token
from arduino_backend.token.schemas import token_schema, token_return_schema

router = APIRouter()


@router.get("/", tags=["token"])
def get_tokens():
    return {"get": "token"}


@router.post("/", tags=["token"])
def add_token(data: token_schema, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    new_token = Token.create(db, data, current_user)
    return_schema = token_return_schema.from_orm(new_token)
    return return_schema


@router.get("/{token_id}", tags=["token"])
def get_single_token():
    return {"single": "token"}


@router.put("/{token_id}", tags=["token"])
def edit_token():
    return {"edit": "token"}


@router.delete("/{token_id}", tags=["token"])
def delete_token():
    return {"delete": "token"}
