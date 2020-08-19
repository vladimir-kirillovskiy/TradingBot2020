import alpaca_trade_api as tradeapi
import websocket
import json
import config
from stop_lose import replace_stop_loss
from Risk import risk
from candlestick import get_dataframe, get_last_price, check_indicator
from close import replace_limit

api = tradeapi.REST(config.KEY_ID, config.SECRET_Key, config.BASE_URL, api_version=config.API_VERSION)

# Ввод нужной акции для работы
print("Введите акцию для отслеживания: ")


# unit = input().lower()

def on_open(ws):
    print("opened")
    auth_data = {
        "action": "authenticate",
        "data": {"key_id": config.KEY_ID, "secret_key": config.SECRET_Key}
    }

    ws.send(json.dumps(auth_data))

    listen_message = {"action": "listen", "data": {"streams": ["AM.AAPL"]}}

    ws.send(json.dumps(listen_message))


def on_message(ws, message):
    print("received a message")
    print(message)
    workplace()


def on_close(ws):
    print("closed connection")


def workplace():
    replace_limit(api)
    watch_list = api.get_watchlist('6281dc22-4ecc-47ab-8239-eba886159ffa')
    dif_symbols = 0
    for each in watch_list.assets:
        dif_symbols = dif_symbols + 1
    print(dif_symbols)
    for each in watch_list.assets:
        unit = each['symbol']
        print('Symbol: ', unit)
        # Получение информации из API ALPACA
        account = api.get_account()
        replace_stop_loss(api)

        # Получение информации из Candlestick
        df = get_dataframe(unit, 100)
        price = get_last_price(df[0], 'c')
        print('Current price: ', price)
        todo = check_indicator(df[0], 'turtle')
        if todo == 'Buy':
            back = 'sell'
        elif todo == 'Sell':
            back = 'buy'
        print('Action: ', todo)
        stop_price, qnty = risk(todo, unit, api)

        print('Stop price: ', stop_price)
        print('Quantity: ', int(qnty))
        total = qnty * price
        money = float(account.buying_power)
        if total > money:
            qnty = money / price
        if stop_price > 0 and qnty > 0:
            try:
                api.submit_order(
                    symbol=unit,
                    qty=int(int(qnty) / dif_symbols),
                    side=todo.lower(),
                    type='market',
                    time_in_force='gtc',
                    order_class='simple')

                api.submit_order(
                    symbol=unit,
                    qty=int(int(qnty) / dif_symbols),
                    side=back,
                    type='limit',
                    time_in_force='gtc',
                    order_class='simple',
                    limit_price=df[0]['close'])
            except Exception as error:
                print(error)


socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()
