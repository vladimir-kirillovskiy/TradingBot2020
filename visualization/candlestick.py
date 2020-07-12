import datetime
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc

import config, requests, json, pandas as pd

minute_bars_url = config.BARS_URL + '/day?symbols=AAPL&limit=10'
r = requests.get(minute_bars_url, headers = config.HEADERS)
data = json.dumps(r.json(), indent=4)
with open('data.txt', 'w') as output:
    output.write(data)
with open('data.txt') as input:
    data = json.load(input)
data_dict = {'t':[], 'o':[], 'h':[], 'l':[], 'c':[]}

for elem in data['AAPL']:
    data_dict['t'].append(datetime.datetime.fromtimestamp(elem['t']))
    data_dict['o'].append(elem['o'])
    data_dict['h'].append(elem['h'])
    data_dict['l'].append(elem['l'])
    data_dict['c'].append(elem['c'])
data = pd.DataFrame(data_dict)
data['t'] = data['t'].map(mdates.date2num)
print(data)


ax = plt.subplot()
ax.grid(True)
ax.set_axisbelow(True)
ax.set_title('AAPL Price', color = 'white')
ax.xaxis_date()
ax.set_facecolor('black')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis = 'x', colors = 'white')
ax.tick_params(axis = 'y', colors = 'white')

candlestick_ohlc(ax, data.values, width=0.5, colorup='#00ff00')

plt.show()