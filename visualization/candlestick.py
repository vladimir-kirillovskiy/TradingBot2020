import plotly.graph_objects as go
import datetime
import config, requests, json, pandas as pd


# Функция возвращает значение ATR для данных из функции set_ATR
def wwma(values, n):
    return values.ewm(alpha=1 / n, adjust=False).mean()


# Задает данные для функции wwma и возвращает столбец с данными ATR
def set_ATR(n):
    high = data['h']
    low = data['l']
    close = data['c']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    return atr

# Функция записывает в data информацию обо всех индикаторах
def set_indicators(n1, n2, n3, n4):
    data['cmean' + str(n1)] = data['c'].rolling(n1).mean()
    data['cmean' + str(n2)] = data['c'].rolling(n2).mean()
    data['llow' + str(n3)] = data['l'].rolling(n3).min()
    data['llow' + str(n4)] = data['l'].rolling(n4).min()
    data['hhigh' + str(n3)] = data['h'].rolling(n3).max()
    data['hhigh' + str(n4)] = data['h'].rolling(n4).max()


TICKERS = 'AAPL'  # Указать интересующие тикеры, если нужно несколько, то перечислить через запятую (Пока работает
# только для 1)
LIMIT = 500  # Количество интервалов для отображения
# Настройка показателей индикаторов
n1 = 10
n2 = 50
nmax = max(n1, n2)
n3 = 21
n4 = 52
nmax2 = max(n3, n4)
INDICATOR = 'hhll'  # Указываем какой индикатор показывать (ma - средние, hhll - минимумы)
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
set_indicators(n1, n2, n3, n4)
data['ATR'] = set_ATR(15)
data_draw = data.tail(LIMIT - nmax + 1)

# Создание графика Candlestick по данным из DataFrame

candlestick = go.Candlestick(x=data_draw['t'], open=data_draw['o'], high=data_draw['h'], low=data_draw['l'],
                             close=data_draw['c'])
figure = go.Figure(data=[candlestick])
figure.layout.xaxis.type = 'category'


# Функция для создания индикаторов всех типов, здесь обновляется data, добавляются столбцы с индикаторами
def create_moving_average_indicator(n, maxn, color, column):
    return create_trace(data['t'][maxn - 1:], data[column][maxn - 1:], color, n)


# Функция для создание линии отображения индикаторов на графике
def create_trace(x, y, color, n):
    return {
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


if INDICATOR == 'ma':
    figure.add_trace(create_moving_average_indicator(n1, nmax, '#3859ff', 'cmean' + str(n1)))
    figure.add_trace(create_moving_average_indicator(n2, nmax, '#000000', 'cmean' + str(n2)))
elif INDICATOR == 'hhll':
    figure.add_trace(create_moving_average_indicator(n3, nmax2, '#ff0000', 'llow' + str(n3)))
    figure.add_trace(create_moving_average_indicator(n4, nmax2, '#000000', 'llow' + str(n4)))
    figure.add_trace(create_moving_average_indicator(n3, nmax2, '#ff0000', 'hhigh' + str(n3)))
    figure.add_trace(create_moving_average_indicator(n4, nmax2, '#000000', 'hhigh' + str(n4)))
figure.show()
