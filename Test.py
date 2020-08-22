import alpaca_trade_api as tradeapi 
from alpaca_trade_api import StreamConn
from candlestick import get_dataframe, check_indicator
LIMIT = 100
n1=10
n2=50
wait = 60
api = tradeapi.REST('PKI5VSIHBY5QD660GUDG', '2BSNsP8amM0q7eFk0dq/xV4IOHhcYKQpcaWndd4u', 'https://paper-api.alpaca.markets',api_version='v2')
dif_symbols = 0
trend = 'trend'
clock = api.get_clock()
if clock.is_open:
    pass
else:
    time_to_open = clock.next_open - clock.timestamp
    print(time_to_open)
df = get_dataframe('AAPL',100)
todo = check_indicator(df[0],'hhll')
# Функция на проверку тренда
#df[0]['cmean10'] = df[0]['c'].rolling(n1).mean()
#df[0]['cmean50'] = df[0]['c'].rolling(n2).mean()
print('CMEAN10:', df[0].iloc[-1]['cmean10'])
trend10 = df[0].iloc[-1]['cmean']


print(asset)
