import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn
import time
wait = 60
api = tradeapi.REST('API_KEY', 'SEKRET_KEY', 'https://paper-api.alpaca.markets',api_version='v2')

print("Введите акцию для отслеживания: ")
unit = input().upper()

while True:    
    barset = api.get_barset(unit, '1Min', limit=5)
    aapl_bars = barset[unit]
    aapl_asset = api.get_asset(unit)
    price = aapl_bars[-1].c
    #print(price)
    if (price < 100 and aapl_asset.tradable):
        api.submit_order(symbol=unit,qty=1,side='buy',type='limit',time_in_force='gtc',limit_price=100)
    time.sleep(wait)




