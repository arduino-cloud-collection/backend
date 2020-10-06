from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, load_only
from src import database


class User(database.DatabaseBase):
    __tablename__ = "users"
    returnFields = ["username", "id"]

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    salt = Column(String)

    @staticmethod
    def get_users(db: Session):
        users = db.query(User).options(load_only(*User.returnFields)).all()
        return users

    @staticmethod
    def get_user(db: Session, username: str):
        user = db.query(User).filter(User.username == username).options(load_only(*User.returnFields)).first()
        return user


database.DatabaseBase.metadata.create_all(bind=database.engine)
