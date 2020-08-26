import alpaca_trade_api as tradeapi
import websocket
import json
import config
from replace_stop_loss import replace_stop_loss
from Risk import risk
from candlestick import get_dataframe, get_last_price, check_indicator
from close import replace_limit

api = tradeapi.REST(config.KEY_ID, config.SECRET_Key, config.BASE_URL, api_version=config.API_VERSION)


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
    clock = api.get_clock()
    if clock.is_open:
        try:
            replace_limit(api)
            print("replace_limit ok")
        except Exception as error:
            print(error)

        watch_list = api.get_watchlists()
        watch_list = watch_list[0].id
        mylist = api.get_watchlist(watch_list)
        dif_symbols = len(mylist.assets)
        print('Number of symbols: ', dif_symbols)
        for each in mylist.assets:
            unit = each['symbol']
            print('Symbol: ', unit)
            # Получение информации из API ALPACA
            account = api.get_account()
            print('get_account ok')

            # Получение информации из Candlestick
            limit = 100
            df = get_dataframe(unit, LIMIT=limit)
            price = get_last_price(df, 'c')
            print('Current price: ', price)
            todo = check_indicator(df, 'turtle')
            if todo == 'Buy':
                back = 'sell'
            elif todo == 'Sell':
                back = 'buy'
            print('Action: ', todo)
            stop_price, qnty = risk(todo, unit, api)
            qnty = int(qnty)

            print('Stop price: ', stop_price)
            print('Quantity: ', qnty)
            total = qnty * price
            money = float(account.buying_power)
            if total > money:
                qnty = int(money/price)
            if stop_price > 0 and qnty > 0:
                try:
                    api.submit_order(
                        symbol=unit,
                        qty=int(int(qnty) / dif_symbols),
                        side=todo.lower(),
                        type='market',
                        time_in_force='gtc',
                        order_class='oto',
                        stop_loss={'stop_price': stop_price})
                except Exception as error:
                    print(error)
                try:
                    api.submit_order(
                        symbol=unit,
                        qty=int(int(qnty) / dif_symbols),
                        side=back,
                        type='limit',
                        time_in_force='gtc',
                        order_class='simple',
                        limit_price=df['close'].iloc[-1])
                except Exception as error:
                    print(error)
    else:
        print('Рынок закрыт')
        print(clock.next_open)


socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()
