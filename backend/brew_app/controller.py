from __future__ import annotations
from datetime import datetime, timedelta
from brew_app.models import State, ProgramStep

# TODO wait during mesh in and mesh out
HYSTERESIS = 0.5


class BrewController:
    def __init__(self):
        self.program: list[ProgramStep] = [
            ProgramStep(name="Mesh In", temperature=45.0, time=10.0,
                        pump_state=False, wait=True, fixed=True),
            ProgramStep(name="Protease", temperature=54.0, time=5.0),
            ProgramStep(name="Combi", temperature=68.0, time=60.0),
            ProgramStep(name="Mesh Out", temperature=78.0, time=15.0,
                        fixed=True, wait=True, pump_state=False),
            ProgramStep(name="Boil", temperature=100.0,
                        time=75.0, fixed=True, pump_state=False),
        ]
        print(self.program)
        self.step = None
        self.step_start_time = None

        self.is_pump_state = False
        self.set_pump_state = False
        self.is_temp = None
        self.set_temp = 0.0
        self.set_time = timedelta(0)

    @property
    def elapsed_time(self) -> timedelta:
        if self.step_start_time:
            now = datetime.now()
            return now - self.step_start_time
        return timedelta(0)

    @property
    def remaining_time(self) -> timedelta:
        if self.step is not None:
            return self.set_time - self.elapsed_time
        return timedelta(0)

    @property
    def set_state(self) -> State:
        return State(self.set_temp, self.set_pump_state)

    @set_state.setter
    def set_state(self, state: State):
        self.set_temp = state.temperature
        self.set_pump_state = state.pump_state
        self.set_time = state.remaining_time

    @property
    def is_state(self) -> State:
        return State(
            temperature=self.is_temp,
            pump_state=self.is_pump_state,
            remaining_time=self.remaining_time,
            step_idx=self.step
        )

    @is_state.setter
    def is_state(self, state: State):
        self.is_temp = state.temperature
        self.is_pump_state = state.pump_state

    def start(self):
        if not self.program:
            raise ValueError("A program must be set first.")
        self.step = -1
        self.next_step()

    def next_step(self):
        self.step += 1
        if self.step == len(self.program):
            self.step = None
            self.program = []
            self.set_temp = 0
            self.set_time = timedelta(0)
            self.step_start_time = None
        else:
            prgrm = self.program[self.step]
            self.set_temp = prgrm.temperature
            self.set_time = timedelta(minutes=prgrm.time)
            self.set_pump_state = prgrm.pump_state
            self.step_start_time = datetime.now()

    def update_internal_state(self):
        if self.remaining_time < timedelta(0):
            self.next_step()


brew_controller = BrewController()


async def controller() -> BrewController:
    return brew_controller
