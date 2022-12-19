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

order_book  = client.order_book()

print('Order Book',order_book)

print('positions',client.positions())

