from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.schemas import user as userSchema
from src.crud import user as userCrud
from src import database

router = APIRouter()


@router.post("/", tags=["auth"])
def create_user(user: userSchema.User, db: Session = Depends(database.get_db)):
    return userCrud.create_user(db=db, user=user)
