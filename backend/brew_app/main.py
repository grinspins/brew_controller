import asyncio
from fastapi import FastAPI, WebSocket, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from brew_app.models import State, ProgramStep
from brew_app.controller import BrewController, controller, brew_controller

ticks: set[asyncio.Task] = set()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex="http://localhost:\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def stop_tick():
    for task in ticks:
        task.cancel()
    ticks = set()


async def tick():
    brew_controller.update_internal_state()
    if brew_controller.step is None:
        stop_tick()
        return
    await asyncio.sleep(1)
    task = asyncio.create_task(tick())
    ticks.add(task)
    task.add_done_callback(ticks.discard)


@app.get("/mcu")
async def get_mcu(controller: BrewController = Depends(controller)):
    return controller.set_state.to_struct()


@app.post('/mcu')
async def post_mcu(mcu_state: bytes = Body(), controller: BrewController = Depends(controller)):
    state = State.from_bytes(mcu_state)
    controller.is_state = state
    return controller.set_state.to_struct()


@app.get("/program")
async def get_program(controller: BrewController = Depends(controller)):
    return controller.program


@app.get("/program")
async def post_program(program: list[ProgramStep], controller: BrewController = Depends(controller)):
    controller.program = program
    return controller.program


@app.post('/start')
async def start(controller: BrewController = Depends(controller)):
    if controller.step is not None:
        raise HTTPException(status_code=400, detail="Program already started")
    try:
        controller.start()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    task = asyncio.create_task(tick())
    ticks.add(task)
    task.add_done_callback(ticks.discard)
    return controller.is_state


@app.websocket("/state")
async def websocket_endpoint(websocket: WebSocket, controller: BrewController = Depends(controller)):
    await websocket.accept()
    while True:
        state_data = await websocket.receive_json()
        if state_data:
            # Does this make sense? mixing is state and set state
            state = State.from_dict(state_data)
            controller.set_state = state
        await websocket.send_json(controller.is_state.to_json())
