from fastapi import APIRouter, Depends, HTTPException
from arduino_backend.controller.models import Controller, Pin
from arduino_backend.user.models import User
from arduino_backend.database import get_db
from arduino_backend.controller.schemas import controller_schema, pin_update_schema, controller_return_schema
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
def get_single_controller(controller_id: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)) -> controller_return_schema:
    return_controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        return_schema: controller_return_schema = controller_return_schema.from_orm(return_controller)
        return return_schema
    else:
        raise HTTPException(403)


@router.delete("/{controller_id}", tags=["controller"])
def delete_controller(controller_id: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    return_controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        return_controller.delete(db)
#        return Controller.del_inf_relationship(return_controller.pins)
    else:
        raise HTTPException(403)


@router.put("/{controller_id}", tags=["controller"])
def modify_controller():
    return {"foo": "bar"}


@router.get("/{controller_id}/{pin_name}", tags=["controller"])
def get_pin(controller_id: str, pin_name: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    return_controller: Controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        return return_controller.get_pin(db, pin_name)
    else:
        raise HTTPException(403)


@router.put("/{controller_id}/{pin_name}", tags=["controller"])
def modify_pin(data: pin_update_schema, controller_id: str, pin_name: str, db: Session = Depends(get_db), current_user: User = Depends(User.get_current_user)):
    return_controller: Controller = Controller.get_controller_by_id(db, controller_id)
    if return_controller.owner == current_user:
        pin: Pin = return_controller.get_pin(db, pin_name)
        pin.change_value(db, data.state)
        return pin
    else:
        raise HTTPException(403)
