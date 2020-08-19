import candlestick as candle


def replace_limit(api):
    orders = api.list_orders(status='opened', limit=500)
    for each in orders:
        if each.order_type == 'limit':
            df = candle.get_dataframe(each.symbol, 100)
            api.replace_order(order_id=each.id, limit_price=df[0]['close'])

