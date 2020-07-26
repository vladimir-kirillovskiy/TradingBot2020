import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn
import time, websocket, json 
from Risk import risk
import streaming_data
import config
wait = 60
api = tradeapi.REST('PKI5VSIHBY5QD660GUDG', '2BSNsP8amM0q7eFk0dq/xV4IOHhcYKQpcaWndd4u', 'https://paper-api.alpaca.markets',api_version='v2')


print("Введите акцию для отслеживания: ")
unit = input().upper()

#while True:    
    #barset = api.get_barset(unit, '1Min', limit=5)
    #aapl_bars = barset[unit]
    #aapl_asset = api.get_asset(unit)
    #price = aapl_bars[-1].c
    #print(price)
    #risk = risk(unit)
    #print(risk[1])
    #if (price<risk[0] and aapl_asset.tradable):
        #api.submit_order(symbol=unit,qty=risk[1],side='buy',type='limit',time_in_force='gtc',limit_price=risk[0])
    #time.sleep(wait)
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
    barset = api.get_barset(unit, '1Min', limit=5)
    aapl_bars = barset[unit]
    price = aapl_bars[-1].c
    print(price)
    risks = risk(unit)
    print(risks[1])
    api.submit_order(symbol=unit,qty=risks[1],side='buy',type='limit',time_in_force='gtc',limit_price=risks[0])

    

def on_close(ws):
    print("closed connection")

socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()





