import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn
import time, websocket, json 
import config
from candlestick import get_dataframe, get_last_price
from Risk import risk, risk_buy, risk_sell
wait = 60
api = tradeapi.REST('PKI5VSIHBY5QD660GUDG', '2BSNsP8amM0q7eFk0dq/xV4IOHhcYKQpcaWndd4u', 'https://paper-api.alpaca.markets',api_version='v2')


print("Введите акцию для отслеживания: ")
unit = input().upper()

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
    df = get_dataframe(unit,100)
    price = get_last_price(df,'c')
    
    print(price)
    risks = risk('buy', unit)
    print(risks[1])
    #if (price<10000):
        #api.submit_order(symbol=unit,qty=risks[1],side='buy',type='limit',time_in_force='gtc',limit_price=risks[0])
    #else:
        #print(risks)




def on_close(ws):
    print("closed connection")

socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()






