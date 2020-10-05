from sqlalchemy import Column, Integer, String
from src import database


class User(database.DatabaseBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    salt = Column(String)


database.DatabaseBase.metadata.create_all(bind=database.engine)
