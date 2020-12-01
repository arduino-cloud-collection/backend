from arduino_backend.database import DatabaseBase
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from arduino_backend.token.schemas import token_schema
from arduino_backend.user.models import User
from arduino_backend.controller.models import Controller
from uuid import uuid4


class Token(DatabaseBase):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True)
    name = Column(String(100))
    user_id = Column(String(36), ForeignKey("users.uuid"))
    controller_id = Column(String(36), ForeignKey("controllers.uuid"))

    controller = relationship("Controller", backref="tokens")
    owner = relationship("User", backref="tokens")

    @classmethod
    def create(cls, db: Session, data: token_schema, user: User):
        uuid: str = str(uuid4())
        token_controller: Controller = Controller.get_controller_by_id(db, data.controller_id)
        new_token: Token = Token(uuid=uuid, name=data.name, user_id=user.uuid, controller_id=token_controller.uuid)
        db.add(new_token)
        db.commit()
        return new_token

    @classmethod
    def all(cls, db: Session, user: User):
        tokens = db.query(cls).filter(cls.owner == user).all()
        return tokens
