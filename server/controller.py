from dataclasses import dataclass
import json
import struct
from datetime import datetime, timedelta
from typing import ClassVar


@dataclass
class State:
    temperature: float
    pump_state: bool
    remaining_time: timedelta = None
    # probably need padding
    MCU_STATE_FORMAT: ClassVar[str] = "<f?"

    def __repr__(self):
        return (
            f"<State temperature={self.temperature} pump_state="
            f"{self.pump_state} remaining_time={self.remaining_time}" 
        )

    def to_struct(self):
        return struct.pack(
            State.MCU_STATE_FORMAT,
            self.temperature,
            self.pump_state
        )

    @classmethod
    def from_bytes(cls, binary):
        temperature, pump_state = struct.unpack(State.MCU_STATE_FORMAT, binary)
        return cls(temperature, pump_state)

    def to_json(self):
        return json.dumps({
            "temperature": self.temperature,
            "pump_state": self.pump_state,
            "remaining_time": self.remaining_time.total_seconds() / 60
        })

    @classmethod
    def from_dict(cls, data):
        remaining_time = timedelta(minutes=data["remaining_time"])
        return cls(data["temperature"], data["pump_state"], remaining_time)


class BrewController:
    def __init__(self):
        self.program = []
        self.step = None
        self.step_start_time = None

        self.is_pump_state = False
        self.set_pump_state = False
        self.is_temp = None
        self.set_temp = 0.0
        self.set_time = timedelta(0)

    @property
    def elapsed_time(self):
        if self.step_start_time:
            now = datetime.now()
            return now - self.step_start_time
        return timedelta(0)

    @property
    def remaining_time(self):
        if self.step is not None:
            return self.set_time - self.elapsed_time
        return timedelta(0)

    @property
    def set_state(self):
        return State(self.set_temp, self.set_pump_state)

    @set_state.setter
    def set_state(self, state):
        self.set_temp = state.temperature
        self.set_pump_state = state.pump_state
        self.set_time = state.remaining_time

    @property
    def is_state(self):
        return State(self.is_temp, self.is_pump_state, self.remaining_time)

    @is_state.setter
    def is_state(self, state):
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
            self.set_temp = prgrm["temperature"]
            self.set_time = timedelta(minutes=prgrm["time"])
            self.step_start_time = datetime.now()

    def update_internal_state(self):
        if self.remaining_time < timedelta(0):
            self.next_step()
    

brew_controller = BrewController()