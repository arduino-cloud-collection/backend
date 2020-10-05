from sqlalchemy.orm import Session, load_only

from src.models import user as userModel
from src.schemas import user as userSchema
from src import settings
from blake3 import blake3
from bcrypt import gensalt

returnFields = ["username", "id"]


def hash_password(password: str, salt: str) -> str:
    return blake3(str.encode(password) + str.encode(salt) + str.encode(settings.config.PEPPER)).hexdigest()


def create_user(db: Session, user: userSchema.User):
    salt = gensalt().decode()
    hash = hash_password(user.password, salt)
    new_user = userModel.User(username=user.username, password=hash, salt=salt)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    del new_user.password
    return new_user


def get_users(db: Session):
    users = db.query(userModel.User).options(load_only(*returnFields)).all()
    return users


def get_user(db: Session, username: str):
    user = db.query(userModel.User).filter(userModel.User.username == username).options(
        load_only(*returnFields)).first()
    return user


def delete_user(db: Session, user: userModel.User):
    db.delete(user)
    db.commit()
    return user


def update_user(db: Session, user: userModel.User, data: userSchema.User):
    if "password" in data and data["password"] != "":
        data["salt"] = gensalt().decode()
        data["password"] = hash_password(data["password"], data["salt"])
    db.query(userModel.User).filter(userModel.User.username == user.username).update(data)
    db.commit()
    returnValue = db.query(userModel.User).filter(userModel.User.id == user.id).options(
        load_only(*returnFields)).first()
    del returnValue.password
    return returnValue


# WARNING PLAIN TEXT
def verify_hash(password: str, hashesd_password: str, salt: str) -> bool:
    if hash_password(password, salt) == hashesd_password:
        return True
    else:
        return False


def authentificate_user(db: Session, username: str, password: str):
    user = db.query(userModel.User).filter(userModel.User.username == username).first()
    if not user or not verify_hash(password, user.password, user.salt):
        return False
    else:
        return user


