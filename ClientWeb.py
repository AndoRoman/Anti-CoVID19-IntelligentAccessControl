import json
from websocket import *

ws = create_connection("ws://localhost:8000/webSocketServidor", header={"Sec-WebSocket-Protocol": "admin"})

# ws.send("LTCBTC")
while True:
    try:
        # if( ws.recv()):

        result = ws.recv()
        # result = json.loads(result)
        print("Received '%s'" % result)
    except KeyboardInterrupt:
        break

ws.close()
