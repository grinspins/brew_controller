import asyncio
import websockets
from controller import BrewController

controller = BrewController()
    
async def main():
    print('starting up!')
    async with websockets.serve(controller.process_messages, "0.0.0.0", 80):
        await asyncio.Future()  # run forever

asyncio.run(main())