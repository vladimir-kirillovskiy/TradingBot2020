import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn
import time, websocket, json
import os 
import config
import asyncio
from Risk import risk, risk_buy, risk_sell
from candlestick import get_dataframe, get_last_price, check_indicator
api = tradeapi.REST('PKI5VSIHBY5QD660GUDG', '2BSNsP8amM0q7eFk0dq/xV4IOHhcYKQpcaWndd4u', 'https://paper-api.alpaca.markets',api_version='v2')
price = 'no'

# Ввод нужной акции для работы
print("Введите акцию для отслеживания: ")
#unit = input().upper()


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
    print(message)
    workplace()
    
    

def on_close(ws):
    print("closed connection")

def workplace():
    #Получение информации из API ALPACA
    barset = api.get_barset('AAPL','day',limit=5)
    aapl_bars = barset['AAPL']
    print('bars ', aapl_bars[-1].c)
    # Получение информации из Candlestick
    df = get_dataframe('AAPL',100)
    price = get_last_price(df[0],'c')
    print('price ', price)
    todo = check_indicator(df[0],'ma')
    print('todo: ', todo)
    risks = risk(todo, 'AAPL')
    print(risks[1])
    if (price < 10000 and price < risks[0] and todo != "Skip"):
        api.submit_order(symbol='AAPL',qty=risks[1],side=todo,type='limit',time_in_force='gtc',limit_price=risks[0])
    
socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()


