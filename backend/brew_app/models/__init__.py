from __future__ import annotations
import json
import struct
from datetime import timedelta
from typing import ClassVar
from pydantic import BaseModel


class ProgramStep(BaseModel):
    temperature: float
    time: float
    pump_state: float
    name: str


class State(BaseModel):
    temperature: float | None
    pump_state: bool | None
    step_idx: int | None
    remaining_time: timedelta | None = None
    MCU_STATE_FORMAT: ClassVar[str] = "<f?"

    def __repr__(self) -> str:
        return (
            f"<State temperature={self.temperature} pump_state="
            f"{self.pump_state} remaining_time={self.remaining_time}"
        )

    def to_struct(self) -> bytes:
        return struct.pack(
            State.MCU_STATE_FORMAT,
            self.temperature,
            self.pump_state
        )

    @classmethod
    def from_bytes(cls: State, binary: bytes) -> State:
        temperature, pump_state = struct.unpack(State.MCU_STATE_FORMAT, binary)
        return cls(temperature, pump_state)

    def to_json(self) -> str:
        return json.dumps({
            "temperature": self.temperature,
            "pump_state": self.pump_state,
            "remaining_time": self.remaining_time.total_seconds() / 60
        })

    @classmethod
    def from_dict(cls: State, data: dict) -> State:
        remaining_time = timedelta(minutes=data["remaining_time"])
        return cls(data["temperature"], data["pump_state"], remaining_time)
