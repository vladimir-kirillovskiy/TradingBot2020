from candlestick import get_last_ATR, get_dataframe, get_last_price
import alpaca_trade_api as tradeapi

# аргументом функции является название акции

def stop_loss(action, stock):
    if action == 'Buy':
        return stop_loss_buy(stock)
    elif action == 'Sell' :
        stop_loss_sell(stock)
    elif action == 'Skip' :
        pass
    else :
        return 'error, action must be buy or sell'
        
        
        
def stop_loss_buy(stock):
    api = tradeapi.REST(
        'PKATONHW8O227OL86EIT', # сюда вставляем  свой key
        'SSt0X7PItaNTMKKW13ObZ3y9NwCsLPsnNkGxH91X', #cюда вставляем свой secret key
        'https://paper-api.alpaca.markets'
    )
    account = api.get_account()
    df, time = get_dataframe(stock, 500)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    money_on_account = account.last_equity
    positions=api.list_positions()
    ppos, time = get_dataframe(positions, 500)
    risk=0
    percent_risk=0.05
    """for i in range len(api.list_positions()) :
        risk=ppos[i]+risk
    if risk<=money_on_account*percent_risk:
        if price < float(money_on_account)*percent:
            stop = price - 2 * atr
            return stop
        else :
            return 0"""
       


def stop_loss_sell(stock):
    api = tradeapi.REST(
        'PKATONHW8O227OL86EIT', # сюда вставляем  свой key
        'SSt0X7PItaNTMKKW13ObZ3y9NwCsLPsnNkGxH91X', #cюда вставляем свой secret key
        'https://paper-api.alpaca.markets'
    )
    account = api.get_account()
    df, time = get_dataframe(stock, 500)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    money_on_account = account.last_equity
    percent=0.01
    positions=api.list_positions()
    ppos, time = get_dataframe(positions, 500)
    risk=0
    percent_risk=0.05
    """for i in range len(api.list_positions()) :
        risk=ppos[i]+risk
    if risk<=money_on_account*percent_risk:
        if price > float(money_on_account)*percent:
            stop = price + 2 * atr
            return stop
        else :
            return 0"""
