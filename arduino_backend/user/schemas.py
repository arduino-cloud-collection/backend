from pydantic import BaseModel


class User(BaseModel):
    username: str = None
    password: str = None

    def check_content(self) -> bool:
        if self.password is None or self.username is None:
            return False
        else:
            return True


class UserLogin(BaseModel):
    username: str
