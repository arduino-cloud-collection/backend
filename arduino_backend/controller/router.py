from fastapi import APIRouter, Depends, HTTPException
from arduino_backend.controller.models import Controller, Pin
from arduino_backend.user.models import User
from arduino_backend.database import get_db
from arduino_backend.controller.schemas import controller_schema, pin_update_schema, controller_return_schema, pin_return_schema
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()


@router.get("/", tags=["controller"])
def get_controllers(db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    controllers: List[Controller] = Controller.get_user_controllers(db, current_user)
    controllerSchemas: List[controller_return_schema] = controller_return_schema.list_parse(controllers)
    return controllerSchemas


@router.post("/", tags=["controller"])
def create_new_controller(data: controller_schema, db: Session = Depends(get_db),
                          current_user: User = Depends(User.get_current_user)) -> controller_return_schema:
    new_controller: Controller = Controller.create_controller(db, data, current_user.uuid)
    return controller_return_schema.from_orm(new_controller)


@router.get("/{controller_id}", tags=["controller"])
def get_single_controller(controller_id: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)) -> controller_return_schema:
    return_controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        return_schema: controller_return_schema = controller_return_schema.from_orm(return_controller)
        return return_schema
    else:
        raise HTTPException(403)


@router.delete("/{controller_id}", tags=["controller"])
def delete_controller(controller_id: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)) -> controller_return_schema:
    return_controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        return_controller.delete(db)
        del_controller_schema: controller_return_schema = controller_return_schema.from_orm(return_controller)
        return del_controller_schema
    else:
        raise HTTPException(403)


@router.put("/{controller_id}", tags=["controller"])
def modify_controller():
    return {"foo": "bar"}


@router.get("/{controller_id}/{pin_name}", tags=["controller"])
def get_pin(controller_id: str, pin_name: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)) -> pin_return_schema:
    return_controller: Controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        pin: Pin = return_controller.get_pin(db, pin_name)
        pin_schema: pin_return_schema = pin_return_schema.from_orm(pin)
        return pin_schema
    else:
        raise HTTPException(403)


@router.put("/{controller_id}/{pin_name}", tags=["controller"])
def modify_pin(data: pin_update_schema, controller_id: str, pin_name: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)) -> pin_return_schema:
    return_controller: Controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        pin: Pin = return_controller.get_pin(db, pin_name)
        pin.change_state(db, data.state)
        pin_schema: pin_return_schema = pin_return_schema.from_orm(pin)
        return pin_schema
    else:
        raise HTTPException(403)
