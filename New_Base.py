import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn
import time
wait = 60
api = tradeapi.REST('API_KEY', 'SEKRET_KEY')

print("Введите акцию для отслеживания: ")
unit = input().upper()

while True:
    barset = api.get_barset(unit, '1Min', limit=5)
    aapl_bars = barset[unit]
    price = aapl_bars[-1].c
    #print(price)
    time.sleep(wait)




