from datetime import datetime, timedelta
from brew_app.models import State, ProgramStep, McuState, SetState

HYSTERESIS = 0.5

mock_p = 0.5
mock_i = 0.05
mock_d = 0.001
i_err = 0.0
last_err = 0.0


def mock_temp(c):
    global i_err
    global last_err
    err = c.set_temp - (c.is_temp or 0.0)
    i_err += err
    d_err = last_err - err
    return mock_p * err + mock_i * i_err + mock_d * d_err


def timedelta_minutes(td: timedelta | None) -> float | None:
    if td is None:
        return None
    return td.total_seconds() / 60


class BrewController:
    def __init__(self):
        self.program: list[ProgramStep] = [
            ProgramStep(
                name="Mesh In",
                temperature=45.0,
                time=10.0,
                pump_state=False,
                wait=True,
            ),
            ProgramStep(name="Protease", temperature=54.0, time=5.0),
            ProgramStep(name="Combi", temperature=68.0, time=60.0),
            ProgramStep(
                name="Mesh Out",
                temperature=78.0,
                time=15.0,
                wait=True,
                pump_state=False,
            ),
            ProgramStep(name="Boil", temperature=100.0, time=75.0, pump_state=False),
        ]

        self.step = None
        self.step_start_time: None | datetime = None

        self.is_pump_state = False
        self.set_pump_state = False
        self.is_temp = 0.0
        self.set_temp = 0.0
        self.duration: timedelta | None = None
        self.is_heating = False

    @property
    def elapsed_time(self) -> timedelta:
        if self.step_start_time:
            now = datetime.now()
            return now - self.step_start_time
        return timedelta(0)

    @property
    def remaining_time(self) -> float | None:
        if self.step is not None:
            delta = self.duration - self.elapsed_time
            return timedelta_minutes(delta)
        return None

    @property
    def mcu_state(self) -> McuState:
        return McuState(temperature=self.set_temp, pump_state=self.set_pump_state)

    @property
    def set_state(self) -> SetState:
        minutes = timedelta_minutes(self.duration)
        return SetState(
            temperature=self.set_temp, pump_state=self.set_pump_state, duration=minutes
        )

    @set_state.setter
    def set_state(self, state: SetState):
        duration = None
        if state.duration is not None:
            duration = timedelta(minutes=state.duration)
        self.set_temp = state.temperature
        self.set_pump_state = state.pump_state
        self.duration = duration

    @property
    def is_state(self) -> State:
        self.is_temp = mock_temp(self)
        return State(
            temperature=self.is_temp,
            pump_state=self.is_pump_state,
            remaining_time=self.remaining_time,
            step_idx=self.step,
            heating=self.is_heating,
        )

    @is_state.setter
    def is_state(self, state: McuState):
        self.is_temp = state.temperature
        self.is_pump_state = state.pump_state

    def start(self):
        if not self.program:
            raise ValueError("A program must be set first.")
        self.step = -1
        self.next_step()

    def next_step(self):
        self.step += 1
        try:
            prgrm = self.program[self.step]
            self.set_temp = prgrm.temperature
            self.duration = timedelta(minutes=prgrm.time)
            self.set_pump_state = prgrm.pump_state
            self.is_heating = True
            self.step_start_time = None
        except KeyError:
            self.stop()

    def stop(self):
        self.step = None
        self.program = []
        self.set_temp = 0
        self.duration = None
        self.step_start_time = None
        self.is_heating = False

    def update_internal_state(self):
        if self.is_temp + HYSTERESIS >= self.set_temp:
            if self.is_heating is True:
                self.step_start_time = datetime.now()
            self.is_heating = False
        remaining_time = self.remaining_time
        if remaining_time and remaining_time < 0:
            self.next_step()


brew_controller = BrewController()


async def controller() -> BrewController:
    return brew_controller
