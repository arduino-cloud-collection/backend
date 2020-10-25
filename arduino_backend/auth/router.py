from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import arduino_backend.user.models
from arduino_backend import database, settings
from arduino_backend.auth import schemas as authSchema

router = APIRouter()


@router.post("/", tags=["auth"], response_model=authSchema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = arduino_backend.user.models.User.authenticate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = arduino_backend.user.models.User.create_access_token(
        data={"user": user.uuid}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
