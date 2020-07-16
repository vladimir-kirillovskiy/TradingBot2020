import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn


api = tradeapi.REST('API_KEY', 'API_SEKRET_KEY')

print("Введите акцию для отслеживания: ")
unit = input().upper()
while True:
    barset = api.get_barset(unit, '1Min', limit=5)
    aapl_bars = barset[unit]

    price = aapl_bars[-1].c
    #print(price)


