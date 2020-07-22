from visualization.candlestick import *
df, time = get_dataframe('AAPL', 500, '2019-04-15T09:30:00-04:00', '2019-04-15T09:50:00-04:00')
print(df)
print(type(get_last_ATR(df)))
print(type(get_last_price(df, 'c')))
print(type(get_last_price(df, 'o')))