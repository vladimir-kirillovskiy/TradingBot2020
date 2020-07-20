from visualization.candlestick import get_last_ATR, get_dataframe, get_last_price
import pandas as pd
times = pd.Series([get_dataframe('AAPL', 500)[1] for i in range(50)], [i for i in range(50)])
print("Среднее время получения данных:", times.mean)
df, time = get_dataframe('AAPL', 500)
print(get_last_ATR(df))
print(get_last_price(df, 'c'))
print(get_last_price(df, 'o'))