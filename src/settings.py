from os import environ


class EnvConfig:
    def __init__(self):
        self.DATABASE_URL = self._get_env("DATABASE_URL")
        self.JWT_KEY = self._get_env("JWT_KEY")
        self.ALGORITHM = self._get_env("ALGORITHM")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(self._get_env("ACCESS_TOKEN_EXPIRE_MINUTES"))

    def _get_env(self, env: str):
        try:
            env_var = environ[env]
        except KeyError:
            raise Exception("The enviroment variable " + env + " cannot be empty")
        return env_var


config = EnvConfig()
