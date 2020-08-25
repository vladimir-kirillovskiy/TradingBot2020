from candlestick import get_last_ATR, get_dataframe, get_last_price
import alpaca_trade_api as tradeapi
from stop_loss import stop_loss_buy, stop_loss_sell
# аргументом функции является название акции


def risk(action, stock, api):
    if action.lower() == 'buy':
        print('risk buy')
        return risk_buy(stock, api)
    elif action.lower() == 'sell':
        print('risk sell')
        return risk_sell(stock, api)
    elif action.lower() == 'skip':
        print('risk skip')
        return 0, 0
    else:
        return 'error, action must be buy or sell'
        
def delete_all_positions(api):
    print('delete all positions')
    api.close_all_positions()
        
def risk_buy(stock, api):
    account = api.get_account()
    money_on_account = float(account.buying_power)
    df = get_dataframe(stock, LIMIT=100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    print('risk: get_last_price ok')
    percent_risk = 0.05
    price_pos = 0
    general_risk = 0
    positions = api.list_positions()
    orders = api.list_orders()
    print('risk: list_orders ok')
    for stock in positions:
        price_pos = stock.avg_entry_price
        print('price_pos = ', price_pos)
        stop_price_list = list(filter(lambda x: x.symbol == stock.symbol, orders))
        if stop_price_list:
            stop_price = list(filter(lambda x: x.symbol == stock.symbol, orders))[0].stop_price
        else:
            stop_price = 0
        print('stop_price = ', stop_price)
        qty = stock.qty
        print('qty = ', qty)
        risk = (float(price_pos) - float(stop_price)) *int(qty)
        print('risk = ', risk)
        general_risk += risk
    if general_risk <= money_on_account * percent_risk:
        print('general_risk <= money*percent')
        stop = price - 2 * atr
        onePercentFromTotal = money_on_account * 0.01
        return stop, onePercentFromTotal / (2 * atr) 
    else:
        print('risk buy else')
        return 0,0
      


def risk_sell(stock, api):
    account = api.get_account()
    money_on_account = float(account.buying_power)
    df= get_dataframe(stock, 100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    print('risk: get_last_price ok')
    percent_risk = 0.05
    price_pos = 0
    general_risk = 0
    positions = api.list_positions()
    orders = api.list_orders()
    print('risk: list_orders ok')
    for stock in positions:
        price_pos = stock.avg_entry_price
        print('price_pos = ', price_pos)
        stop_price_list = list(filter(lambda x: x.symbol == stock.symbol, orders))
        if stop_price_list:
            stop_price = list(filter(lambda x: x.symbol == stock.symbol, orders))[0].stop_price
        else:
            stop_price = 0
        qty = stock.qty
        print('qty = ', qty)
        risk = (float(price_pos) - float(stop_price)) *int(qty)
        print('risk = ', risk)
        general_risk += risk
    if general_risk <= money_on_account * percent_risk:
        print('general_risk <= money*percent')
        stop = price + 2 * atr
        onePercentFromTotal = money_on_account * 0.01
        return stop, onePercentFromTotal / (2 * atr)
    else:
        print('risk sell else')
        return 0, 0
        







