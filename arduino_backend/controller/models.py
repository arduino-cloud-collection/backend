from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship
from uuid import uuid4
from typing import List

from arduino_backend.database import DatabaseBase
from arduino_backend.controller.schemas import controller_schema, pin_schema
from arduino_backend.user.models import User


class Controller(DatabaseBase):
    __tablename__ = "controllers"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True)
    name = Column(String(100))
    user_id = Column(String(36), ForeignKey("users.uuid"))

    owner = relationship("User", back_populates="controllers")

    @classmethod
    def get_user_controllers(cls, db: Session, user: User):
        controllers = db.query(cls).filter(cls.owner == user).all()
        for i in controllers:
            cls.del_inf_relationship(i.pins)
        return controllers

    @staticmethod
    def del_inf_relationship(pins: List):
        for i in pins:
            del i.controller

    @classmethod
    def get_controller_by_id(cls, db: Session, controller_id: str):
        controller = db.query(cls).filter(cls.uuid == controller_id).first()
        cls.del_inf_relationship(controller.pins)
        return controller

    @classmethod
    def create_controller(cls, db: Session, data: controller_schema, user_id: User.uuid):
        uuid = str(uuid4())
        new_controller = Controller(uuid=uuid, name=data.name, user_id=user_id)
        for i in range(9):
            Pin.create_pin(db, pin_schema(name="D" + str(i)), new_controller.uuid)
        db.add(new_controller)
        db.commit()
        return new_controller


class Pin(DatabaseBase):
    __tablename__ = "pins"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True)
    name = Column(String)
    controller_id = Column(String(36), ForeignKey(Controller.uuid))

    controller = relationship("Controller", backref="pins")

    @classmethod
    def create_pin(cls, db: Session, data: pin_schema, controller_id: Controller.uuid):
        uuid = str(uuid4())
        pin = Pin(uuid=uuid, name=data.name, controller_id=controller_id)
        db.add(pin)
        db.commit()
        return pin
