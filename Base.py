def workplace():
    clock = api.get_clock()
    if clock.is_open:

        replace_stop_loss(api)
    
        watch_list = api.get_watchlists()
        watch_list = watch_list[0].id
        mylist = api.get_watchlist(watch_list)
    
        dif_symbols = len(mylist.assets)
        print('Number of symbols: ', dif_symbols)

        for each in mylist.assets:


            unit = each['symbol']
            print('Symbol: ', unit)
            account = api.get_account()


            df = get_dataframe(unit,100)
            print(df[0].iloc[-1])
            price = get_last_price(df[0],'c')
            print('Current price: ', price)

            todo = check_indicator(df[0],'hhll')

            #df[0]['cmean10'] = df[0]['c'].rolling(n1).mean()
            #df[0]['cmean50'] = df[0]['c'].rolling(n2).mean()
            trend10 = df[0].iloc[-1]['cmean100']
            trend50 = df[0].iloc[-1]['cmean50']
            if (trend10 > trend50 and todo == 'Buy'):
                todo = 'Buy'
            elif (trend10 < trend50 and todo == 'Sell'):
                todo = 'Sell'
            else:
                todo = 'Skip'
            print('Action: ', todo)


            stop_price, qnty = risk(todo, unit,api)
            qnty = int(qnty)
            print('Stop price: ', stop_price)
            print('Quantity: ', int(qnty))

            total = qnty * price
            money = float(account.buying_power)

            if total>money:
                qnty = int(money/price)
            if (qnty>0):
                try:
                    api.submit_order(
                        symbol=unit,
                        qty=int(qnty/dif_symbols),
                        side=todo.lower(),
                        type='market',
                        time_in_force='gtc',
                        order_class='oto',
                        stop_loss={'stop_price':stop_price})
                except Exception as error:
                    print(error)


        
    
socket = "wss://data.alpaca.markets/stream"

ws = websocket.WebSocketApp(socket, on_open=on_open, on_message=on_message, on_close=on_close)
ws.run_forever()
