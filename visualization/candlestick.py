import plotly.graph_objects as go
import datetime
import config, requests, json, pandas as pd

TICKERS = 'AAPL' # Указать интересующие тикеры, если нужно несколько, то перечислить через запятую (Пока работает
# только для 1)
LIMIT = 100 # Количество интервалов для отображения

# Получаем данные с Alpaca о текущем состоянии

minute_bars_url = config.BARS_URL + '/day?symbols={}&limit={}'.format(TICKERS,LIMIT)
r = requests.get(minute_bars_url, headers = config.HEADERS)
data = json.dumps(r.json(), indent=4)

# Записываем их в файл, затем считываем в формате json
with open('data.txt', 'w') as output:
    output.write(data)
with open('data.txt') as input:
    data = json.load(input)

data_dict = {'t':[], 'o':[], 'h':[], 'l':[], 'c':[]} # Словарь для создания DataFrame

# На основании информации заполняем data_dict, затем создаем DataFrame на его основе

for elem in data[TICKERS]:
    data_dict['t'].append(datetime.datetime.fromtimestamp(elem['t']))
    data_dict['o'].append(elem['o'])
    data_dict['h'].append(elem['h'])
    data_dict['l'].append(elem['l'])
    data_dict['c'].append(elem['c'])
data = pd.DataFrame(data_dict)
data_draw = data.tail(LIMIT-49)

# Создание графика Candlestick по данным из DataFrame

candlestick = go.Candlestick(x=data_draw['t'], open = data_draw['o'], high= data_draw['h'], low= data_draw['l'], close= data_draw['c'])
figure = go.Figure(data=[candlestick])
figure.layout.xaxis.type = 'category'

# Настройка первого индикатора

x10 = []
y10 = []
for i in range(50, LIMIT+1):
    y10.append(data.loc[i-10:i-1]['c'].mean())
    x10.append(data.iloc[i-1]['t'])
trace1 = {
  "x": x10,
  "y": y10,
  "line": {
    "color": "#3859ff",
    "width": 2
  },
  "mode": "lines",
  "name": "MA10",
  "type": "scatter",
}

# Настройка второго индикатора

x50 = []
y50 = []
for i in range(50, LIMIT+1):
    y50.append(data.loc[i-50:i-1]['c'].mean())
    x50.append(data.iloc[i-1]['t'])
trace2 = {
  "x": x50,
  "y": y50,
  "line": {
    "color": "#385965",
    "width": 2
  },
  "mode": "lines",
  "name": "MA50",
  "type": "scatter",
}

figure.add_trace(trace1)
figure.add_trace(trace2)
figure.show()
