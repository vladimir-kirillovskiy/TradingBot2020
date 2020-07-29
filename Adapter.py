tradeapi.REST(Key, SecretKey, 'https://paper-api.alpaca.markets', api_version='v2') #Аутентификация

def account_state(Key, SecretKey):  # Состояние счета
        api = tradeapi.REST(Key, SecretKey, 'https://paper-api.alpaca.markets')
        account = api.get_account()
        return account.last_equity

api.list_orders()  # Получение всех открытых заявок

api.replace_order()  # Обновление стоп лосса

api.submit_order()


