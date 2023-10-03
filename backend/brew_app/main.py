import asyncio
from fastapi import FastAPI, WebSocket, Depends, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from brew_app.models import State, ProgramStep, McuState, SetState
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
async def get_mcu(controller: BrewController = Depends(controller)) -> bytes:
    return controller.mcu_state.to_struct()


@app.post("/mcu")
async def post_mcu(
    mcu_state: bytes = Body(), controller: BrewController = Depends(controller)
) -> bytes:
    state = McuState.from_bytes(mcu_state)
    controller.is_state = state
    return controller.mcu_state.to_struct()


@app.get("/program")
async def get_program(
    controller: BrewController = Depends(controller),
) -> list[ProgramStep]:
    return controller.program


@app.post("/program")
async def post_program(
    program: list[ProgramStep], controller: BrewController = Depends(controller)
) -> list[ProgramStep]:
    controller.program = program
    return controller.program


@app.post("/start")
async def start(controller: BrewController = Depends(controller)) -> State:
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


@app.get("/set_state")
async def get_set_state(controller: BrewController = Depends(controller)) -> SetState:
    return controller.set_state


@app.post("/set_state")
async def post_set_state(
    state: SetState, controller: BrewController = Depends(controller)
) -> SetState:
    controller.set_state = state
    return controller.set_state


@app.websocket("/state")
async def state_socket(
    websocket: WebSocket, controller: BrewController = Depends(controller)
):
    await websocket.accept()
    while True:
        await websocket.receive_text()
        await websocket.send_json(controller.is_state.model_dump())
