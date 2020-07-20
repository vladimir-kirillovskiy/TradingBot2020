from visualization.candlestick import get_last_ATR, get_dataframe, get_last_price
df = get_dataframe('DIS', 500)
print(get_last_ATR(df))
print(get_last_price(df, 'c'))
print(get_last_price(df, 'o'))