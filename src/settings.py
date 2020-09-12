from os import environ


class envConfig:
    def __init__(self):
        try:
            self.DATABASE_URL = environ["DATABASE_URL"]
        except KeyError:
            raise Exception("The Database-URL can't be empty.")
