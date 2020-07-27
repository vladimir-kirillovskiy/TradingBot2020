import datetime
import time

import plotly.graph_objects as go

import config
import json
import pandas as pd
import numpy as np
import requests


# Функция возвращает значение ATR для данных из функции set_ATR
def wwma(values, n):
    return values.ewm(alpha=1 / n, adjust=False).mean()


# Задает данные для функции wwma и возвращает столбец с данными ATR
def set_ATR(data, n):
    high = data['h']
    low = data['l']
    close = data['c']
    data['tr0'] = abs(high - low)
    data['tr1'] = abs(high - close.shift())
    data['tr2'] = abs(low - close.shift())
    tr = data[['tr0', 'tr1', 'tr2']].max(axis=1)
    atr = wwma(tr, n)
    data.drop(['tr0', 'tr1', 'tr2'], axis='columns', inplace=True)
    return atr


# Функция записывает в data информацию обо всех индикаторах
def set_indicators(data, n1, n2, n3, n4):
    data['cmean' + str(n1)] = data['c'].rolling(n1).mean()
    data['cmean' + str(n2)] = data['c'].rolling(n2).mean()
    data['llow' + str(n3)] = data['l'].rolling(n3).min()
    data['llow' + str(n4)] = data['l'].rolling(n4).min()
    data['hhigh' + str(n3)] = data['h'].rolling(n3).max()
    data['hhigh' + str(n4)] = data['h'].rolling(n4).max()
    for i in range(1, LIMIT):
        if (data.loc[i, 'cmean' + str(n1)] - data.loc[i, 'cmean' + str(n2)]) < 0 < (data.loc[i - 1, 'cmean' + str(n1)] - data.loc[i - 1, 'cmean' + str(n2)]):
            data.loc[i, 'ma'] = "Sell"
        elif (data.loc[i, 'cmean' + str(n1)] - data.loc[i, 'cmean' + str(n2)]) > 0 > (data.loc[i - 1, 'cmean' + str(n1)] - data.loc[i - 1, 'cmean' + str(n2)]):
            data.loc[i, 'ma'] = "Buy"
        else:
            data.loc[i, 'ma'] = "Skip"
        if data.loc[i, 'llow' + str(n3)] == data.loc[i, 'llow' + str(n4)] and data.loc[i, 'hhigh' + str(n3)] != data.loc[i, 'hhigh' + str(n4)]:
            data.loc[i, 'hhll'] = "Sell"
        elif data.loc[i, 'hhigh' + str(n3)] == data.loc[i, 'hhigh' + str(n4)] and data.loc[i, 'llow' + str(n3)] != data.loc[i, 'llow' + str(n4)]:
            data.loc[i, 'hhll'] = "Buy"
        else:
            data.loc[i, 'hhll'] = "Skip"


# Функция записывает в data информацию об ATR bands
def set_ATR_bands(data):
    data['ATR_High'] = data[['h', 'ATR']].sum(axis=1)
    data['ATR_Low'] = data['l'] - data['ATR']


# Функция возвращает data со всеми данными по акциям
def get_dataframe(TICKERS, LIMIT, START=None, END=None):
    # Получаем данные с Alpaca о текущем состоянии

    start_time = time.time()
    if START is None and END is None:
        minute_bars_url = config.BARS_URL + '/minute?symbols={}&limit={}'.format(TICKERS, LIMIT)
    else:
        minute_bars_url = config.BARS_URL + '/minute?symbols={}&limit={}&start={}&end={}'.format(TICKERS, LIMIT, START,
                                                                                                 END)
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
    set_indicators(data, n1, n2, n3, n4)
    data['ATR'] = set_ATR(data, 15)
    set_ATR_bands(data)

    return data, time.time() - start_time


TICKERS = 'DIS'  # Указать интересующие тикеры, если нужно несколько, то перечислить через запятую (Пока работает
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


# Функция для создания индикаторов всех типов, здесь обновляется data, добавляются столбцы с индикаторами
def create_moving_average_indicator(data, n, maxn, color, column):
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


# Функция возвращает последнее значение ATR
def get_last_ATR(df):
    return df['ATR'].iloc[-1]


# Функция возвращает последнюю цену (o - открытия, c - закрытия, h - наибольшую, l - наименьшую) Пример в test.py
def get_last_price(df, type):
    return df[type].iloc[-1]


# Функция отображает candlestick график и индикаторы
def visualize(data):
    data_draw = data.tail(LIMIT - nmax + 1)
    candlestick = go.Candlestick(x=data_draw['t'], open=data_draw['o'], high=data_draw['h'], low=data_draw['l'],
                                 close=data_draw['c'])
    figure = go.Figure(data=[candlestick])
    figure.layout.xaxis.type = 'category'
    if INDICATOR == 'ma':
        figure.add_trace(create_moving_average_indicator(data, n1, nmax, '#3859ff', 'cmean' + str(n1)))
        figure.add_trace(create_moving_average_indicator(data, n2, nmax, '#000000', 'cmean' + str(n2)))
    elif INDICATOR == 'hhll':
        figure.add_trace(create_moving_average_indicator(data, n3, nmax2, '#ff0000', 'llow' + str(n3)))
        figure.add_trace(create_moving_average_indicator(data, n4, nmax2, '#000000', 'llow' + str(n4)))
        figure.add_trace(create_moving_average_indicator(data, n3, nmax2, '#ff0000', 'hhigh' + str(n3)))
        figure.add_trace(create_moving_average_indicator(data, n4, nmax2, '#000000', 'hhigh' + str(n4)))
    figure.show()


# Функция проверяет является ли последняя цена сигналом на покупку / продажу
def check_indicator(df, type):
    if type == 'ma':
        return df.tail(1)['ma'].iloc[0]
    elif type == 'hhll':
        return df.tail(1)['hhll'].iloc[0]


data, time = get_dataframe(TICKERS, LIMIT)
print(check_indicator(data, 'hhll'))