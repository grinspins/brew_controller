import json
from datetime import datetime, timedelta


class BrewController:
    def __init__(self):
        self.program = []
        self.step = 0
        self.time_left = None
        self.pump_state = True

    def process_message(self, websocket, message):
        type, *message = message.split(';')
        match type:
            case "set":
                self.process_set(websocket, message)
            case "get":
                pass
            case "init":
                self.initialize(websocket, message)

    def initialize(self, websocket, message):
        content = json.loads(message)
        for step in content:
            temperature = step['temperature']
            time_min = step['time']
            self.program.append(dict(
                temperature = int(temperature),
                time = timedelta(minutes=time_min)
            ))
        self.time_left = self.program[self.step]['time']
        self.send_set_points(websocket)

    def send_set_points(self, websocket):
        websocket.send('does this even work without async??')


        

