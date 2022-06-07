# import json
# import websocket
# import numpy as np
# import pandas as pd
# import config
# import Processes
#
# socket = "wss://api.alpaca.markets/stream"
# socket2 = "wss://data.alpaca.markets/stream"
# socket3 = "wss://stream.data.alpaca.markets/v2/IEX"
# # socket2 = "wss://stream.data.alpaca.markets/v2/IEX"
#
# authorisation = {"action": "authenticate","data": {"key_id": "PKAW1YWRR8APK57ZRN0F","secret_key": "cAxQ2tbAAbwYOLRbtXypbJ4K7YJmlMxghiIFj0lP"}}
#
#
# def on_open():
#     print("message")
#
#
# def on_message():
#     print("message")
#
#
# def on_close():
#     print("message")
#
#
# # websocket.enableTrace(True)
# ws = websocket.WebSocketApp(socket, on_open=on_open)
# ws.run_forever()
#
# def on_open(ws):
#     print("opened")
#     # ws.send(json.dumps(authorisation))
#     # channel_data = {"action": "subscribe", "params": "AM.TSLA"}
#     # ws.send(json.dumps(channel_data))
#
#
# def on_message(ws, message):
#     print("you recieved a message!!")
#     print(message)
#
#
# def on_close(ws):
#     print("connection closed")
#
#
# ws = websocket.WebSocketApp(socket3, on_open=on_open)
# ws.run_forever()


# import config
# import websocket, json
#
#
# def on_open(ws):
#     print("opened")
#     auth_data = {
#         "action": "authenticate",
#         "data": {"key_id": config.API_KEY, "secret_key": config.SECRET_KEY}
#     }
#
#     ws.send(json.dumps(auth_data))
#
#     listen_message = {"action": "listen", "data": {"streams": ["AM.TSLA"]}}
#
#     ws.send(json.dumps(listen_message))
#
#
# def on_message(ws, message):
#     print("received a message")
#     print(message)
#
#
# def on_close(ws):
#     print("closed connection")
#
#
# socket = "wss://data.alpaca.markets/stream"
#
# ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
# ws.run_forever()


import threading
import alpaca_trade_api as tradeapi
import config

BASE_URL = "https://paper-api.alpaca.markets"

conn = tradeapi.stream2.StreamConn(config.API_KEY, config.SECRET_KEY, BASE_URL)


@conn.on(r'^trade_updates$')
async def on_trade_updates(conn, channel, trade):
    print('trade', trade)


def ws_start():
    print("yeo")
    conn.run(['account_updates', 'trade_updates'])


# start WebSocket in a thread
ws_thread = threading.Thread(target=ws_start, daemon=True)
ws_thread.start()
