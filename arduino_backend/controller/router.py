from fastapi import APIRouter, Depends
from arduino_backend.controller.models import Controller
from arduino_backend.user.models import User
from arduino_backend.database import get_db
from arduino_backend.controller.schemas import controller_schema
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", tags=["controller"])
def get_controllers(db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    return Controller.get_user_controllers(db, current_user)


@router.post("/", tags=["controller"])
def create_new_controller(data: controller_schema, db: Session = Depends(get_db),
                          current_user: User = Depends(User.get_current_user)):
    return Controller.create_controller(db, data, current_user.uuid)
