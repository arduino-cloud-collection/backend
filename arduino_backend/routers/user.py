from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import arduino_backend.models.user
from arduino_backend import database
from arduino_backend.models import user as userModels
from arduino_backend.schemas import user as userSchema

router = APIRouter()


@router.post("/", tags=["user"])
def create_user(user: userSchema.User, db: Session = Depends(database.get_db)):
    return arduino_backend.models.user.User.create_user(db=db, user=user)


@router.get("/", tags=["user"])
def get_users(db: Session = Depends(database.get_db)):
    return userModels.User.get_users(db=db)


@router.get("/{username}", tags=["user"])
def get_user_by_name(username: str, db: Session = Depends(database.get_db)):
    user = arduino_backend.models.user.User.get_user(db=db, username=username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user


@router.delete("/{username}", tags=["user"])
def delete_user(username: str, db: Session = Depends(database.get_db)):
    user = arduino_backend.models.user.User.get_user(db=db, username=username)
    return user.delete(db=db)


@router.put("/{username}", tags=["user"])
def update_user(username: str, data: userSchema.User, db: Session = Depends(database.get_db)):
    partial_data = data.dict(exclude_unset=True)
    user = arduino_backend.models.user.User.get_user(db=db, username=username)
    return user.update_user(db=db, data=partial_data)
