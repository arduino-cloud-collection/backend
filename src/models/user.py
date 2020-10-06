from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, load_only
from src import database
from src.schemas import user as userSchema


class User(database.DatabaseBase):
    __tablename__ = "users"
    returnFields = ["username", "id"]

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    salt = Column(String)

    @classmethod
    def get_users(cls, db: Session):
        users = db.query(cls).options(load_only(*cls.returnFields)).all()
        return users

    @classmethod
    def get_user(cls, db: Session, username: str):
        user = db.query(cls).filter(cls.username == username).options(load_only(*cls.returnFields)).first()
        return user

    def delete(self, db: Session, user: userSchema.User):
        db.delete(self)
        db.commit()
        return self


database.DatabaseBase.metadata.create_all(bind=database.engine)
