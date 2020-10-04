from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str = None
    password: str = None


class UserLogin(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None
