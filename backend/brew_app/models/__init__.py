import struct
from pydantic import BaseModel

MCU_STATE_FORMAT: str = "<f?"


class ProgramStep(BaseModel):
    temperature: float
    time: float
    pump_state: bool = False
    name: str
    wait: bool = False


class SetState(BaseModel):
    temperature: float
    pump_state: bool
    duration: int | None


class McuState(BaseModel):
    temperature: float
    pump_state: bool

    @classmethod
    def from_bytes(cls: "State", binary: bytes) -> "State":
        temperature, pump_state = struct.unpack(MCU_STATE_FORMAT, binary)
        return cls(temperature, pump_state)

    def to_struct(self) -> bytes:
        return struct.pack(MCU_STATE_FORMAT, self.temperature, self.pump_state)


class State(BaseModel):
    temperature: float | None
    pump_state: bool | None
    step_idx: int | None = None
    remaining_time: int | None = None
