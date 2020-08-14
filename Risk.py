from candlestick import get_last_ATR, get_dataframe, get_last_price
import alpaca_trade_api as tradeapi
from stop_loss import stop_loss_buy, stop_loss_sell
# аргументом функции является название акции


def risk(action, stock, api):
    if action.lower() == 'buy':
        return risk_buy(stock, api)
    elif action.lower() == 'sell' :
        return risk_sell(stock, api)
    elif action.lower() == 'skip' :
        return 0, 0
    else :
        return 'error, action must be buy or sell'
        
def delete_all_positions(api):
    api.close_all_positions()
        
def risk_buy(stock, api):
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
        
