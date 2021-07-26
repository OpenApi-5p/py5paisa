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
user=YOUR_EMAIL_ID
pass=YOUR_LOGIN_PASSWORD
dob=YOUR_DOB
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
Scrip Master - https://www.5paisa.com/docs/default-source/scrip-master/scripmaster-csv-format.csv
#### Placing an order

```py
# Note: This is an indicative order.

from py5paisa.order import Order, OrderType, Exchange

test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code=1660, quantity=1, price=205,is_intraday=True,atmarket=False)
client.place_order(test_order)

```
#### Placing offline orders (After Market Orders)

By default all orders are normal orders, pass `ahplaced=Y` to place offline orders.

```py
from py5paisa.order import Order, OrderType, AHPlaced
test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code=1660, quantity=1, price=205,is_intraday=False,atmarket=False, ahplaced='Y')
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
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=205,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=215.0,TriggerPriceForSL=203,ExchType='C',Exch='N',RequestType='P',AtMarket=False)

client.bo_order(test_order)
```
Note:For placing Bracket order in FNO segment pass ExchType='D'

For Modifying Bracket Order only for Initial order (entry)
```py
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=203,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=208.0,TriggerPriceForSL=202,ExchType='C',Exch='N',RequestType='M',AtMarket=False,ExchOrderId='12345678')

client.bo_order(test_order)

#Note : For cover order just pass LimitPriceProfitOrder equal to Zero.
```

For Modifying LimitPriceProfitOrder 
```py
test_order=Order(order_type='S', scrip_code=1660, quantity=1, price=208.50,is_intraday=True,exchange='N',exchange_segment='C',atmarket=False,exch_order_id="12345678" ,order_for='M')

client.mod_bo_order(test_order)
```
For Modifying TriggerPriceForSL
```py
test_order=Order(order_type='S', scrip_code=1660, quantity=1, price=0,is_intraday=True,exchange='N',exchange_segment='C',atmarket=True,exch_order_id="123456789" ,stoploss_price=201.50,is_stoploss_order=True,order_for='M')

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
Note: Use the following abbreviations :

Market Feed=mf

Market Depth (upto 5)=md

Open Interest=oi

Subscribe= s

Unsubscribe=u

#### Full Market Snapshot 
```py
a=[{"Exchange":"N","ExchangeType":"C","ScripCode":"2885"},
   {"Exchange":"N","ExchangeType":"C","ScripCode":"1660"},
   ]
print(Client.fetch_market_depth(a))
```
#### Historical Data
```py
#historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)

df=Client.historical_data('N','C',1660,'15m','2021-05-25','2021-06-16')
print(df)

# Note : TimeFrame Should be from this list ['1m','5m','10m','15m','30m','60m','1d']
```

#### Strategy Execution
#### List Of Strategies Available
 - Short Straddle
 - Short Strangle
 - Long Straddle
 - Long Strangle
 - Iron Fly(Butterfly)
 - Iron Condor
 - Call Calendar Spread
 - Put Calendar Spread
```py
#Import strategy package
from py5paisa.strategy import *
```
Note: These single-commands are capable of trading multiple legs of pre-defined strategies.
Like :- Short/Long Straddles and Strangles, Iron Fly and Iron Condor (many more to come)
Please use these at your own risk.
```py
#Create an Object:-
strategy=strategies()
```
Use the following to execute the strategy (note:- they are executed at market price only)
```py
#short_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
strategy.short_straddle("banknifty",'37000','50','20210610','I')
```
```py
#short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.short_strangle("banknifty",['35300','37000'],'50','20210610','D')
```
```py
#long_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
strategy.long_straddle("banknifty",'37000','50','20210610','I')
```
```py
#long_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.long_strangle("banknifty",['35300','37000'],'50','20210610','D')
```

```py
#iron_condor(<symbol>,<List of buy strike prices>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.iron_condor("NIFTY",["15000","15200"],["15100","15150"],"75","20210603","I")
```

```py
#iron_fly(<symbol>,<List of buy strike prices>,<Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.iron_fly("NIFTY",["15000","15200"],"15100","75","20210610","I")
```

```py
#call_calendar(<symbol>,<List of sell strike price>,<qty>,<list of expiry(first one will be bought and the second sold based on expiry)>,<Order Type>)
strategy.call_calendar("nifty",'15600','75',['20210603','20210610'],'I')
```

```py
#put_calendar(<symbol>,<List of sell strike price>,<qty>,<list of expiry(first one will be bought and the second sold based on expiry)>,<Order Type>)
strategy.put_calendar("nifty",'15600','75',['20210603','20210610'],'I')
```

```py
#call_ladder(<symbol>,<Buy strike prices>,<List of Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.call_ladder("NIFTY","15100",["15300","15400"],"75","20210610","I")
```

```py
#put_ladder(<symbol>,<Buy strike prices>,<List of Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.put_ladder("NIFTY","15000",["14800","14500"],"75","20210610","I")
```

```py
#ladder(<symbol>,<List of Buy strike prices>,<List of Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.ladder("sbin",["400","420"],["350","370","450","500"],"1500","20210729","D")
```
#### Ideas
```py
print(Client.get_buy())

print(Client.get_trade())

```

#### TODO
 - Write tests.


#### Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
