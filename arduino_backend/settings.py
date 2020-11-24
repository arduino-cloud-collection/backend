from os import getenv


class EnvConfig:
    def __init__(self):
        self.DATABASE_URL = getenv("DATABASE_URL", "sqlite:///test.db")
        self.JWT_KEY = getenv("JWT_KEY", "b7c18b06a0416d6af22bfaf49abaf7b75956056963e3116e3bbff3be72ed20fa")
        self.ALGORITHM = getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 10))
        self.PEPPER = getenv("PEPPER", "hcQoBj+~Z#JxLd0K")


config = EnvConfig()
