from bcrypt import gensalt
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, load_only
from src import database
from blake3 import blake3
from src import settings
from src.schemas import user as userSchema


# Database class for the User model
class User(database.DatabaseBase):
    __tablename__ = "users"
    returnFields = ["username", "id"]

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    salt = Column(String)

    # Returns all users as objects
    @classmethod
    def get_users(cls, db: Session):
        users = db.query(cls).options(load_only(*cls.returnFields)).all()
        return users

    # Returns single user by username
    @classmethod
    def get_user(cls, db: Session, username: str):
        user = db.query(cls).filter(cls.username == username).options(load_only(*cls.returnFields)).first()
        return user

    # Deletes the user from the database
    def delete(self, db: Session):
        db.delete(self)
        db.commit()
        return self

    # Creates a new user and hashes its password
    @classmethod
    def create_user(cls, db: Session, user: userSchema.User):
        salt = gensalt().decode()
        pw_hash = cls.hash_password(user.password, salt)
        new_user = User(username=user.username, password=pw_hash, salt=salt)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        del new_user.password
        del new_user.salt
        return new_user

    # Hash and salt the given password with blake3
    @classmethod
    def hash_password(cls, password: str, salt: str) -> str:
        return blake3(str.encode(password) + str.encode(salt) + str.encode(settings.config.PEPPER)).hexdigest()

    # Updates the user by the given dataset
    def update_user(self, db: Session, data: userSchema.User):
        if "password" in data and data["password"] != "":
            data["salt"] = gensalt().decode()
            data["password"] = self.hash_password(data["password"], data["salt"])
        db.query(User).filter(User.username == self.username).update(data)
        db.commit()
        returnValue = db.query(User).filter(User.id == self.id).options(
            load_only(*self.returnFields)).first()
        del returnValue.password
        del returnValue.salt
        return returnValue

    # Verify password and salt with a given hash
    @classmethod
    def verify_hash(cls, password: str, hashesd_password: str, salt: str) -> bool:
        if cls.hash_password(password, salt) == hashesd_password:
            return True
        else:
            return False

    # Validate user and password
    @classmethod
    def authentificate_user(cls, db: Session, username: str, password: str):
        user = db.query(cls).filter(cls.username == username).first()
        if not user or not cls.verify_hash(password, user.password, user.salt):
            return False
        else:
            return user


database.DatabaseBase.metadata.create_all(bind=database.engine)
