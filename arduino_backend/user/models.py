from datetime import timedelta, datetime
from typing import Optional
from uuid import uuid4

from bcrypt import gensalt
from blake3 import blake3
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, load_only, relationship

from arduino_backend import database
from arduino_backend import settings
from arduino_backend.user import schemas as userSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


# Database class for the User model
class User(database.DatabaseBase):
    __tablename__ = "users"
    returnFields = ["username", "id"]

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    salt = Column(String)

    controllers = relationship("Controller", back_populates="owner")

    # Returns all users as objects
    @classmethod
    def get_users(cls, db: Session):
        users = db.query(cls).options(load_only(*cls.returnFields)).all()
        return users

    # Returns single user by username
    @classmethod
    def get_user(cls, db: Session, username: str):
        user = db.query(cls).filter(cls.username == username).first()
        return user

    @classmethod
    def get_user_by_uuid(cls, db: Session, uuid: str):
        user = db.query(cls).filter(cls.uuid == uuid).options(load_only(*cls.returnFields)).first()
        return user

    # Deletes the user from the database
    def delete(self, db: Session):
        db.delete(self)
        db.commit()
        return self

    # Creates a new user and hashes its password
    @classmethod
    def create_user(cls, db: Session, user: userSchema.User):
        if not user.check_content():
            raise HTTPException(status_code=400)
        else:
            salt = gensalt().decode()
            pw_hash = cls.hash_password(user.password, salt)
            new_user = User(username=user.username, password=pw_hash, salt=salt, uuid=str(uuid4()))
            try:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return_user = cls.get_user_by_uuid(db=db, uuid=new_user.uuid)
                return return_user
            except IntegrityError:
                raise HTTPException(status_code=400)

    # Hash and salt the given password with blake3
    @classmethod
    def hash_password(cls, password: str, salt: str) -> str:
        return blake3(str.encode(password) + str.encode(salt) + str.encode(settings.config.PEPPER)).hexdigest()

    # Updates the user by the given dataset
    def update_user(self, db: Session, data: userSchema.User):
        if "password" in data and data["password"] != "":
            data["salt"] = gensalt().decode()
            data["password"] = self.hash_password(data["password"], data["salt"])
        try:
            db.query(User).filter(User.username == self.username).update(data)
            db.commit()
            returnValue = db.query(User).filter(User.id == self.id).options(
                load_only(*self.returnFields)).first()
            return returnValue
        except IntegrityError:
            raise HTTPException(status_code=400)

    # Verify password and salt with a given hash
    @classmethod
    def verify_hash(cls, password: str, hashed_password: str, salt: str) -> bool:
        return cls.hash_password(password, salt) == hashed_password

    # Validate user and password
    @classmethod
    def authenticate_user(cls, db: Session, username: str, password: str):
        user = db.query(cls).filter(cls.username == username).first()
        if not user or not cls.verify_hash(password, user.password, user.salt):
            return False
        else:
            return user

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.config.JWT_KEY, algorithm=settings.config.ALGORITHM)
        return encoded_jwt

    @classmethod
    def decode_token(cls, token):
        try:
            payload = jwt.decode(token, settings.config.JWT_KEY, algorithms=[settings.config.ALGORITHM])
            body: str = payload.get("user")
        except JWTError:
            body = False
        return body

    @classmethod
    def get_current_user(cls, token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
        uuid = cls.decode_token(token)
        if uuid:
            try:
                user = cls.get_user_by_uuid(db, uuid)
                return user
            except IntegrityError:
                raise HTTPException(status_code=403)
        else:
            raise HTTPException(status_code=403)

