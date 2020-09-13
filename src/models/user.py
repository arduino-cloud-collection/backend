from sqlalchemy import Column, Integer, String
from src import database


class User(database.DatabaseBase):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36))
    username = Column(String, unique=True, index=True)
    password = Column(String)


database.DatabaseBase.metadata.create_all(bind=database.engine)
