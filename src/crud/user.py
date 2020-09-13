from sqlalchemy.orm import Session
from uuid import uuid4
from src.models import user as userModel
from src.schemas import user as userSchema


def create_user(db: Session, user: userSchema.User):
    new_user = userModel.User(uuid=str(uuid4()), username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
