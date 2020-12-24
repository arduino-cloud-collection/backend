from fastapi import APIRouter, WebSocket


router = APIRouter()


@router.websocket_route("/")
async def client_socket(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_text()
    await websocket.send_text(f"Message text was: {data}")
