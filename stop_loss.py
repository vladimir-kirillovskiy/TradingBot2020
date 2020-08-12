from candlestick import get_last_ATR, get_dataframe, get_last_price
import alpaca_trade_api as tradeapi

# аргументом функции является название акции

def stop_loss(action, stock, api):
    if action.lower() == 'buy':
        return stop_loss_buy(stock, api)
    elif action.lower() == 'sell' :
        return stop_loss_sell(stock, api)
    elif action.lower() == 'skip' :
        pass
    else :
        return 'error, action must be buy or sell'
        
        
        
def stop_loss_buy(stock, api):
    df, time = get_dataframe(stock, 100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    stop = price - 2 * atr
    return stop
      

def stop_loss_sell(stock, api):
    df, time = get_dataframe(stock, 100)
    atr = get_last_ATR(df)
    price = get_last_price(df, 'c')
    stop = price + 2 * atr
    return stop
