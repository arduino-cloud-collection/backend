from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from src.crud import auth as authCrud
from src.schemas import user as userSchema

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


@router.get("/")
async def read_users_me(current_user: userSchema.UserLogin = Depends(authCrud.get_current_user)):
    return current_user
