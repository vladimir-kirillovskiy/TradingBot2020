import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn
import time, websocket, json
import os 
import config
import replace_stop_loss
import asyncio, Risk
from Risk import risk, risk_buy, risk_sell
from candlestick import get_dataframe, get_last_price, check_indicator
api = tradeapi.REST('PKI5VSIHBY5QD660GUDG', '2BSNsP8amM0q7eFk0dq/xV4IOHhcYKQpcaWndd4u', 'https://paper-api.alpaca.markets',api_version='v2')


# Ввод нужной акции для работы
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
    print(message)
    workplace()
    
    

def on_close(ws):
    print("closed connection")

def workplace():
    #Получение информации из API ALPACA
    barset = api.get_barset(unit,'day',limit=5)
    aapl_bars = barset[unit]
    #replace_stop_loss(api)
    print('equity ')
    print('bars ', aapl_bars[-1].c)
    # Получение информации из Candlestick
    df = get_dataframe(unit,100)
    price = get_last_price(df[0],'c')
    print('price ', price)
    todo = check_indicator(df[0],'ma')
    print('todo: ', todo)
    risks = risk(todo, unit)
    print('risks: ', risks)
    if (risks[0]>0 and risks[1]>0):
        #api.submit_order(symbol=unit,qty=qnty,side=todo,type='limit',time_in_force='gtc',limit_price=stop)
    
socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()

