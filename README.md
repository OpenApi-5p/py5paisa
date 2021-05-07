# 5paisa Python SDK

Python SDK for 5paisa APIs natively written in VB .NET

![PyPI](https://img.shields.io/pypi/v/py5paisa)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/5paisa/py5paisa/Publish%20package/master)

![5paisa logo](./docs/images/5-paisa-img.jpg)

#### Documentation

Read the docs hosted [here](https://5paisa.github.io/)

#### Features

-   Order placement, modification and cancellation
-   Fetching user info including holdings, positions, margin and order book.
-   Fetching live market streaming.
-   Placing, modifying and deleting Bracket Order.
-   Fetching order status and trade information.
-   Getting live data streaming using websockets.

### Installation

`pip install py5paisa`

### Usage

#### Configuring API keys

Get your API keys from https://www.5paisa.com/developerapi/apikeys

Configure these keys in a file named `keys.conf` in the same directory as your python script exists

A sample `keys.conf` is given below:

```conf
[KEYS]
APP_NAME=YOUR_APP_NAME_HERE
APP_SOURCE=YOUR_APP_SOURCE_HERE
USER_ID=YOUR_USER_ID_HERE
PASSWORD=YOUR_PASSWORD_HERE
USER_KEY=YOUR_USER_KEY_HERE
ENCRYPTION_KEY=YOUR_ENCRYPTION_KEY_HERE
```


#### Authentication

```py
from py5paisa import FivePaisaClient

client = FivePaisaClient(email="random_email@xyz.com", passwd="password", dob="YYYYMMDD")
client.login()
```

After successful authentication, you should get a `Logged in!!` message
#### Market Feed

```py
#NOTE : Symbol has to be in the same format as specified in the example below.

req_list_=[{"Exch":"N","ExchType":"D","Symbol":"NIFTY 22 APR 2021 CE 15200.00","Expiry":"20210422","StrikePrice":"15200","OptionType":"CE"},
            {"Exch":"N","ExchType":"D","Symbol":"NIFTY 22 APR 2021 PE 15200.00","Expiry":"20210422","StrikePrice":"15200","OptionType":"PE"}]
            
client.fetch_market_feed(req_list_)
```

#### Fetching user info

```py
# Fetches holdings
client.holdings()

# Fetches margin
client.margin()

# Fetches positions
client.positions()

# Fetches the order book of the client
client.order_book()

```

Scrip codes reference:

Note : Use these Links for getting scrip codes

BSE: https://www.bseindia.com/
NSE FO: https://www.5paisa.com/docs/default-source/scrip-master/contract.txt
NSE CASH : https://www.5paisa.com/docs/default-source/scrip-master/security.txt

#### Placing an order

```py
# Note: This is an indicative order.

from py5paisa.order import Order, OrderType, Exchange, ExchangeType

test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code=1660, quantity=1, price=205,is_intraday=True,atmarket=False)
client.place_order(test_order)

```

#### Modifying an order

```py
test_order = Order(order_type='B', scrip_code=1660, quantity=1, price=205,is_intraday=False,exchange='N',exchange_segment='C',atmarket=True,exch_order_id="12345678" )
client.modify_order(test_order)
```

#### Canceling an order

```py
client.cancel_order(order_type='B', scrip_code=1660, quantity=1,exchange='N',exchange_segment='C',exch_order_id='12345678')
```
#### Bracket Order 



For placing Braket order
```py
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=204,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=208.0,TriggerPriceForSL=202,RequestType='P',AtMarket=False)

client.bo_order(test_order)
```
Note:For placing Bracket order in FNO segment pass ExchType='D'

For Modifying Bracket Order only for Initial order (entry)
```py
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=203,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=208.0,TriggerPriceForSL=202,RequestType='M',AtMarket=False,ExchOrderId='12345678')

client.bo_order(test_order)

#Note : For cover order just pass LimitPriceProfitOrder equal to Zero.
```

For Modifying LimitPriceProfitOrder 
```py
test_order=Order(order_type='S', scrip_code=1660, quantity=1, price=208.50,is_intraday=True,exchange='N',exchange_segment='C',atmarket=False,exch_order_id="12345678" ,order_for=OrderFor.MODIFY)

client.mod_bo_order(test_order)
```
For Modifying TriggerPriceForSL
```py
test_order=Order(order_type='S', scrip_code=1660, quantity=1, price=0,is_intraday=True,exchange='N',exchange_segment='C',atmarket=True,exch_order_id="123456789" ,stoploss_price=201.50,is_stoploss_order=True,order_for=OrderFor.MODIFY)

client.mod_bo_order(test_order)

#Note : You have pass atmarket=true while modifying stoploss price, Pass ExchorderId for the particular leg to modify.
```

#### Fetching Order Status and Trade Information

```py
from py5paisa.order import  Exchange

req_list= [

        {
            "Exch": "N",
            "ExchType": "C",
            "ScripCode": 20374,
            "ExchOrderID": "1000000015310807"
        }]

# Fetches the trade details
client.fetch_trade_info(req_list)

req_list_= [

        {
            "Exch": "N",
            "ExchType": "C",
            "ScripCode": 20374,
            "RemoteOrderID": "90980441"
        }]
# Fetches the order status
client.fetch_order_status(req_list_)

```
#### Live Market Feed Streaming

```py
req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":1660},
            
            ]

dict1=Client.Request_Feed('mf','s',req_list)

client.Streming_data(dict1)
```
Note: use the following abbreviations :
Market Feed=mf
Market Depth (upto 5)=md
Open Interest=oi

Subscribe= s
Unsubscribe=u


#### TODO
 - Write tests.


#### Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
