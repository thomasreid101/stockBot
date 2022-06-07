import websocket

socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocket()
ws.connect(socket)