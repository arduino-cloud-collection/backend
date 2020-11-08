from fastapi import APIRouter, Depends
from arduino_backend.controller.models import Controller
from arduino_backend.user.models import User
from arduino_backend.database import get_db
from arduino_backend.controller.schemas import controller_schema
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/", tags=["controller"])
def get_controllers(db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    controller = Controller.get_user_controllers(db, current_user)
    return controller


@router.post("/", tags=["controller"])
def create_new_controller(data: controller_schema, db: Session = Depends(get_db),
                          current_user: User = Depends(User.get_current_user)):
    return Controller.create_controller(db, data, current_user.uuid)


@router.get("/{controller_id}", tags=["controller"])
def get_single_controller():
    return {"foo": "bar"}


@router.delete("/{controller_id}", tags=["controller"])
def delete_controller():
    return {"foo": "bar"}


@router.put("/{controller_id}", tags=["controller"])
def modify_controller():
    return {"foo": "bar"}


@router.get("/{controller_id}/{pin_name}", tags=["controller"])
def get_pin():
    return {"foo": "bar"}


@router.put("/{controller_id}/{pin_name}", tags=["controller"])
def modify_pin():
    return {"foo": "bar"}
