from py5paisa import FivePaisaClient
from py5paisa.strategy import *
from datetime import datetime

cred={
    "APP_NAME":"5P50052770",
    "APP_SOURCE":"10345",
    "USER_ID":"fdiUhA4mBNO",
    "PASSWORD":"jalna7w0RuA",
    "USER_KEY":"giQIoatyGcXADwxV05uWHiOW2QOWNLcs",
    "ENCRYPTION_KEY":"dlXKxViN7yLMIaDc3RpCJzZeqwSvYbu7"
    }

client = FivePaisaClient(email="bhaveshshirode1@gmail.com", passwd="Quant@123", dob="19931214",cred=cred)
client.login()
#df=client.historical_data('N', 'C', 999920000, '15m', '2022-09-09', '2022-09-09')
df=client.historical_data('N','C',22385,'1d','2022-09-15','2022-09-20')
df = client.get_tradebook()
print(client.margin())
print(client.holdings())
print(client.positions())
print(client.order_book())
#print(type(df['TradeBookDetail'][0].get('ExchangeTradeTime')))
print(datetime.now())
#datetime_str = datetime.strftime(df['TradeBookDetail'][0].get('ExchangeTradeTime'),"%d%b%Y%H%M%S")
print(df)


