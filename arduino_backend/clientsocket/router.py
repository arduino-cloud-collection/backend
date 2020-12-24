from fastapi import APIRouter, WebSocket, Depends, status

from arduino_backend.token.models import Token

router = APIRouter()


@router.websocket_route("/")
async def client_socket(websocket: WebSocket, token: str = Depends(Token.get_token)):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")
