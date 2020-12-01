from arduino_backend.database import DatabaseBase
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import Session, relationship


class Token(DatabaseBase):
    __tablename__ = "tokens"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String(36), unique=True)
    name = Column(String(100))
    user_id = Column(String(36), ForeignKey("users.uuid"))
    controller_id = Column(String(36), ForeignKey("controllers.uuid"))

    controller = relationship("Controller", backref="tokens")
    owner = relationship("User", backref="tokens")
