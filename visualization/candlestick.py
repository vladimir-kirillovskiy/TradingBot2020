import plotly.graph_objects as go
import datetime
import config, requests, json, pandas as pd

TICKERS = 'DIS'  # Указать интересующие тикеры, если нужно несколько, то перечислить через запятую (Пока работает
# только для 1)
LIMIT = 500  # Количество интервалов для отображения
# Настройка показателей индикаторов
n1 = 10
n2 = 50
nmax = max(n1, n2)
# Получаем данные с Alpaca о текущем состоянии

minute_bars_url = config.BARS_URL + '/minute?symbols={}&limit={}'.format(TICKERS, LIMIT)
r = requests.get(minute_bars_url, headers=config.HEADERS)
data = json.dumps(r.json(), indent=4)

# Записываем их в файл, затем считываем в формате json
with open('data.txt', 'w') as output:
    output.write(data)
with open('data.txt') as input:
    data = json.load(input)

data_dict = {'t': [], 'o': [], 'h': [], 'l': [], 'c': []}  # Словарь для создания DataFrame

# На основании информации заполняем data_dict, затем создаем DataFrame на его основе

for elem in data[TICKERS]:
    data_dict['t'].append(datetime.datetime.fromtimestamp(elem['t']))
    data_dict['o'].append(elem['o'])
    data_dict['h'].append(elem['h'])
    data_dict['l'].append(elem['l'])
    data_dict['c'].append(elem['c'])
data = pd.DataFrame(data_dict)
data_draw = data.tail(LIMIT - nmax + 1)

# Создание графика Candlestick по данным из DataFrame

candlestick = go.Candlestick(x=data_draw['t'], open=data_draw['o'], high=data_draw['h'], low=data_draw['l'],
                             close=data_draw['c'])
figure = go.Figure(data=[candlestick])
figure.layout.xaxis.type = 'category'


# Функция для создания индикаторов и их отображения
def create_indicator(n, nmax, color):
    x = []
    y = []
    for i in range(nmax, LIMIT + 1):
        y.append(data.loc[i - n:i - 1]['c'].mean())
        x.append(data.iloc[i - 1]['t'])
    trace = {
        "x": x,
        "y": y,
        "line": {
            "color": color,
            "width": 2
        },
        "mode": "lines",
        "name": "MA" + str(n),
        "type": "scatter",
    }
    return trace


figure.add_trace(create_indicator(n1, nmax, '#3859ff'))
figure.add_trace(create_indicator(n2, nmax, '#000000'))
figure.show()
