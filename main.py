from fastapi import FastAPI, HTTPException, Request, Websocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# middleware 설정
app.add_middleware( # cors middleware
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = set()

@app.websocket("/ws")
async def websocket_endpoint(websocket: Websocket):
    await websocket.accept()
    connected_clients.add(websocket)
    try:
        while True:
            # 클라이언트로부터 메시지를 수신
            message = await websocket.receive_text()
            print(f"Received message from client: {message}")
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        print("Client disconnected")

@app.post("/broadcast")
async def broadcast_message(data: dict):
    """
    WebSocket 클라이언트들에게 브로드캐스트
    """
    if not connected_clients:
        return JSONResponse(status_code=400, content={"message": "No clients connected"})
    message = data.get("message") or data
    for client in connected_clients:
        try:
            await client.send_json(message)
        except Exception as e:
            print(f"Failed to send message to client: {e}")
            connected_clients.remove(client)
    return {"status": "success", "message": "Message broadcasted successfully"}