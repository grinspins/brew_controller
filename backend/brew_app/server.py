import json
from flask import Flask, request, abort
from controller import brew_controller, State

app = Flask(__name__)


@app.route('/mcu', methods=['GET', 'POST'], endpoint='mcu')
def micro_controller():
    brew_controller.update_internal_state()
    if request.method == 'POST':
        state = State.from_bytes(request.get_data())
        brew_controller.is_state = state
    return brew_controller.set_state.to_struct()


@app.route('/program', methods=['GET', 'POST'], endpoint='program')
def program():
    if request.method == 'POST':
        program = request.get_json()
        brew_controller.program = program
    return json.dumps(brew_controller.program)


@app.route('/state', methods=['GET', 'POST'], endpoint='state')
def state():
    brew_controller.update_internal_state()
    if request.method == 'POST':
        state = State.from_dict(request.get_json())
        brew_controller.set_state = state
    return brew_controller.is_state.to_json()


@app.route('/start', methods=['POST'], endpoint='start')
def start():
    if brew_controller.step is not None:
        abort(400, "Program already started")
    brew_controller.start()
    return brew_controller.is_state.to_json()


if __name__ == '__main__':
    app.run('0.0.0.0', 80, debug=True)