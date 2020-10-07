from os import getenv


class EnvConfig:
    def __init__(self):
        self.DATABASE_URL = getenv("DATABASE_URL")
        self.JWT_KEY = getenv("JWT_KEY")
        self.ALGORITHM = getenv("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        self.PEPPER = getenv("PEPPER")


config = EnvConfig()
