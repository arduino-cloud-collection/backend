from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from uuid import uuid4

from arduino_backend.database import DatabaseBase
from arduino_backend.controller.schemas import controller_schema
from arduino_backend.user.models import User


class Controller(DatabaseBase):
    __tablename__ = "controllers"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True)
    name = Column(String(100))
    user = Column(String(36), ForeignKey(User.uuid))

    @classmethod
    def get_user_controllers(cls, db: Session, user: User):
        return db.query(cls).filter(cls.user == user.uuid).all()

    @classmethod
    def create_controller(cls, db: Session, data: controller_schema, user_id: User.uuid):
        uuid = str(uuid4())
        new_controller = Controller(uuid=uuid, name=data.name, user=user_id)
        db.add(new_controller)
        db.commit()
        return new_controller


class Pin(DatabaseBase):
    __tablename__ = "pins"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True)
    name = Column(String)
    controller = Column(String(36), ForeignKey(Controller.uuid))
