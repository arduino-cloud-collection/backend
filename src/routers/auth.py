from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from src.crud import auth as authCrud
from sqlalchemy.orm import Session
from src.schemas import auth as authSchema
from src.crud import user as userCrud
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from src import database, settings

router = APIRouter()


@router.post("/", tags=["auth"], response_model=authSchema.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = userCrud.authentificate_user(db=db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = authCrud.create_access_token(
        data={"user": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}