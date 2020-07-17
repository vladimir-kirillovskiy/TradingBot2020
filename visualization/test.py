from visualization.candlestick import get_last_ATR, get_dataframe
df = get_dataframe('DIS', 500)
print(get_last_ATR(df))