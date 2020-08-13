from candlestick import get_last_ATR, get_dataframe, get_last_price
import alpaca_trade_api as tradeapi
from stop_loss import stop_loss_buy, stop_loss_sell
# аргументом функции является название акции


def risk(action, stock, api):
    if action == 'Buy':
        return risk_buy(stock, api)
    elif action == 'Sell' :
        return risk_sell(stock, api)
    elif action == 'Skip' :
        pass
    else :
        return 'error, action must be buy or sell'
        
def delete_all_positions(api):
    api.close_all_positions()
        
def risk_buy(stock, api):
    account = api.get_account()
    money_on_account = float(account.last_equity)
    df, time = get_dataframe(stock, 100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    percent_risk = 0.05
    price_pos = 0
    general_risk = 0
    positions = api.list_positions()
    orders = api.list_orders()
    for stock in positions:
        price_pos = stock.avg_entry_price
        stop_price = list(filter(lambda x: x.symbol == stock.symbol, orders))[0].stop_price
        qty = stock.qty
        risk = (int(price_pos) - int(stop_price)) *int(qty)
        general_risk += risk
    if general_risk <= money_on_account * percent_risk:
        stop = price - 2 * atr
        onePercentFromTotal = money_on_account * 0.01
        return stop, onePercentFromTotal / (2 * atr) 
      


def risk_sell(stock, api):
    account = api.get_account()
    money_on_account = float(account.buying_power)
    df, time = get_dataframe(stock, 100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    percent_risk = 0.05
    price_pos = 0
    general_risk = 0
    positions = api.list_positions()
    orders = api.list_orders()
    for stock in positions:
        price_pos = stock.avg_entry_price
        stop_price = list(filter(lambda x: x.symbol == stock.symbol, orders))[0].stop_price
        qty = stock.qty
        risk = (int(price_pos) - int(stop_price)) *int(qty)
        general_risk += risk
    if general_risk <= money_on_account * percent_risk:
        stop = price + 2 * atr
        onePercentFromTotal = money_on_account * 0.01
        return stop, onePercentFromTotal / (2 * atr) 
        
def risk_buy_alternative(stock,api):
    account = api.get_account()
    money_on_account = float(account.buying_power)
    df, time = get_dataframe(stock, 100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    percent_risk = 0.05
    money_on_account_start = 100000
    ppos = money_on_account_start - money_on_account
    stop = price - 2 * atr
    risk = ppos - stop
    if risk <= money_on_account*percent_risk:
        onePercentFromTotal = money_on_account*0.01
        return stop, onePercentFromTotal / (2*atr)    #сколько акций мы можем себе позволить, учитывая стоп лосс
      


def risk_sell_alternative(stock,api):
    account = api.get_account()
    money_on_account = float(account.buying_power)
    df, time = get_dataframe(stock, 100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    stop = price + 2 * atr
    risk = price - stop
    percent_risk = 0.05
    money_on_account_start = 100000
    ppos = money_on_account_start - money_on_account
    p = price + 2 * atr
    risk = ppos - stop
    if risk <= money_on_account*percent_risk:
        onePercentFromTotal = money_on_account*0.01
        return stop, onePercentFromTotal / (2*atr)    #сколько акций мы можем себе позволить, учитывая стоп лосс
