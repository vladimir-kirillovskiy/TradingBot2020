import config
import websocket, json, requests
import pandas

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": config.KEY_ID, "secret_key": config.SECRET_Key}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["AM.AAPL"]}}

    ws.send(json.dumps(listen_message))
   


def on_message(ws, message):
    print("received a message")
    #print(message)
    minute_bars_url = config.BARS_URL + '/1Min?symbols=AAPL&limit=1'
    r = requests.get(minute_bars_url, headers=config.HEADERS)
    print(json.dumps(r.json(),indent=4))
    

def on_close(ws):
    print("closed connection")

socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()