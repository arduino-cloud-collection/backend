from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas import user as userSchema
from src.crud import user as userCrud
from src import database
import logging

router = APIRouter()


@router.post("/", tags=["user"])
def create_user(user: userSchema.User, db: Session = Depends(database.get_db)):
    return userCrud.create_user(db=db, user=user)


@router.get("/", tags=["user"])
def get_users(db: Session = Depends(database.get_db)):
    return userCrud.get_users(db=db)


@router.get("/{username}", tags=["user"])
def get_user_by_name(username: str, db: Session = Depends(database.get_db)):
    user = userCrud.get_user(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.delete("/{username}", tags=["user"])
def delete_user(username: str, db: Session = Depends(database.get_db)):
    user = userCrud.get_user(db=db, username=username)
    return userCrud.delete_user(db=db, user=user)
