import plotly.graph_objects as go
import datetime
import config, requests, json, pandas as pd

TICKERS = 'AAPL' # Указать интересующие тикеры, если нужно несколько, то перечислить через запятую (Пока работает
# только для 1)
LIMIT = 100 # Количество интервалов для отображения

# Получаем данные с Alpaca о текущем состоянии

minute_bars_url = config.BARS_URL + '/minute?symbols={}&limit={}'.format(TICKERS,LIMIT)
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

# Создание графика Candlestick по данным из DataFrame

candlestick = go.Candlestick(x=data['t'], open = data['o'], high= data['h'], low= data['l'], close= data['c'])
figure = go.Figure(data=[candlestick])
figure.layout.xaxis.type = 'category'
figure.show()