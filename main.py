from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn

app = FastAPI()

# middleware 설정
app.add_middleware( # cors middleware
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

connected_clients = {}

@app.get("/health")
async def health_check():
    return {"status": "ok"}

async def broadcast_message(message: str):
    for client_id, websocket in connected_clients.items():
        try:
            await websocket.send_text(message)
        except Exception as e:
            print(f"Failed to send message to client {client_id}: {e}")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    client_id = id(websocket)
    connected_clients[client_id] = websocket

    try:
        while True:
            message = await websocket.receive_text()
            print(f"Received message from client: {message}")

            await broadcast_message(message)
            print(f"send message from client: {message}")
    except WebSocketDisconnect:
        del connected_clients[client_id]
        print("Client disconnected")
    except Exception as e:
        print(f"Error with client {client_id}: {e}")
    finally:
        if client_id in connected_clients:
            del connected_clients[client_id]
        print(f"Client {client_id} removed. Total clients: {len(connected_clients)}")
        
Instrumentator().instrument(app).expose(app)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=9000, reload=True)