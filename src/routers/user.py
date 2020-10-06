from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import src.models.user
from src import database
from src.crud import user as userCrud
from src.models import user as userModels
from src.schemas import user as userSchema

router = APIRouter()


@router.post("/", tags=["user"])
def create_user(user: userSchema.User, db: Session = Depends(database.get_db)):
    return userCrud.create_user(db=db, user=user)


@router.get("/", tags=["user"])
def get_users(db: Session = Depends(database.get_db)):
    return userModels.User.get_users(db=db)


@router.get("/{username}", tags=["user"])
def get_user_by_name(username: str, db: Session = Depends(database.get_db)):
    user = src.models.user.User.get_user(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.delete("/{username}", tags=["user"])
def delete_user(username: str, db: Session = Depends(database.get_db)):
    user = src.models.user.User.get_user(db=db, username=username)
    return userCrud.delete_user(db=db, user=user)


@router.put("/{username}", tags=["user"])
def update_user(username: str, data: userSchema.User, db: Session = Depends(database.get_db)):
    partial_data = data.dict(exclude_unset=True)
    user = src.models.user.User.get_user(db=db, username=username)
    return userCrud.update_user(db=db, user=user, data=partial_data)
