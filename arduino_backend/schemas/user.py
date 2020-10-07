from pydantic import BaseModel


class User(BaseModel):
    username: str = None
    password: str = None


class UserLogin(BaseModel):
    username: str
