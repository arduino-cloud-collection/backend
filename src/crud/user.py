from sqlalchemy.orm import Session, load_only
from src.models import user as userModel
from src.schemas import user as userSchema

returnFields = ["username", "id"]


def create_user(db: Session, user: userSchema.User):
    new_user = userModel.User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
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
    db.query(userModel.User).filter(userModel.User.username == user.username).update(data)
    db.commit()
    returnValue = db.query(userModel.User).filter(userModel.User.id == user.id).options(load_only(*returnFields)).first()
    del returnValue.password
    return returnValue
