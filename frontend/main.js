const websocket = new WebSocket("ws://localhost:8000");

const program  = [
    {temperature: 10, time: 10},
    {temperature: 20, time: 15}
]

const msg = `init;${JSON.stringify(program)}`

function send() {
    if (websocket.readyState == 1) {
        console.log('sending')
        websocket.send(msg);
    } else {
        console.log('waitng')
    }
    
}

setInterval(send, 5000);



