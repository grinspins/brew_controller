import json
from fastapi import FastAPI, WebSocket, Depends
from controller import BrewController, controller

app = FastAPI()


@app.get("/program")
async def get(controller: BrewController = Depends(controller)):
    return json.dumps(controller.program)


@app.get("/program")
async def get(program, controller: BrewController = Depends(controller)):
    controller.program = program
    return json.dumps(controller.program)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        await websocket.send_json(data)
