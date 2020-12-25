import asyncio
from json import JSONDecodeError

from fastapi import APIRouter, WebSocket, Depends, status
from fastapi_sqlalchemy import db
from pydantic.error_wrappers import ValidationError
from websockets.exceptions import ConnectionClosedError

from arduino_backend.clientsocket.schemas import auth_schema
from arduino_backend.controller.models import Controller
from arduino_backend.controller.schemas import controller_schema, controller_return_schema
from arduino_backend.token.models import Token

router = APIRouter()


@router.websocket_route("/")
async def client_socket(websocket: WebSocket):
    with db():
        await websocket.accept()
        try:
            auth_data: auth_schema = auth_schema(**await websocket.receive_json())
            controller_class = Token.get_controller_by_token(db.session, auth_data.key)
            controller: controller_return_schema = controller_return_schema \
                .from_orm(controller_class)
            await websocket.send_json(controller.json())
            while True:
                try:
                    await asyncio.sleep(1)
                    session = db.session
                    controller_update_schema = controller_return_schema.from_orm(controller_return_schema.from_orm(Controller.get_controller_by_id(session, controller.uuid)))
                    if controller_update_schema.json() != controller.json():
                        controller = controller_update_schema
                        await websocket.send_json(controller.json())
                    session.close()
                except ConnectionClosedError:
                    break
        except JSONDecodeError:
            await websocket.close(code=1007)
        except ValidationError:
            await websocket.close(code=1007)
