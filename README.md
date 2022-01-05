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

Get your API keys from https://invest.5paisa.com/DeveloperAPI/APIKeys

Note:- We have deprecated the existing method which involved the use of keys.conf file.
       Kindly go through this updated documentation.

#### Authentication

```py
from py5paisa import FivePaisaClient
cred={
    "APP_NAME":"YOUR APP_NAME",
    "APP_SOURCE":"YOUR APP_SOURCE",
    "USER_ID":"YOUR USER_ID",
    "PASSWORD":"YOUR PASSWORD",
    "USER_KEY":"YOUR USERKEY",
    "ENCRYPTION_KEY":"YOUR ENCRYPTION_KEY"
    }

client = FivePaisaClient(email="random_email@xyz.com", passwd="password", dob="YYYYMMDD",cred=cred)
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

# Fetches Trade book
client.get_tradebook()

```

Scrip codes reference:

Note : Use these Links for getting scrip codes

Scrip Master - https://images.5paisa.com/website/scripmaster-csv-format.csv
#### Placing an order

```py
# Note: This is an indicative order.

from py5paisa.order import Order, OrderType, Exchange

#This is example of a commodity order. You can pass scripdata either you can pass scripcode also.

#Using Scrip Data :-

test_order = Order(order_type='B',exchange='M',exchange_segment='D', scripdata = 'GOLDM 03 Nov 2021_20211103', quantity=1, price=47900,is_intraday=True,IsGTCOrder=False,IsEOSOrder=True)
client.place_order(test_order)

#Using Scrip Code :-
test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code = 1660, quantity=1, price=236.5,is_intraday=True)
client.place_order(test_order)

```
#### Placing offline orders (After Market Orders)

By default all orders are normal orders, pass `ahplaced=Y` to place offline orders.

```py
from py5paisa.order import Order, OrderType, AHPlaced
test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code=1660, quantity=1, price=205,is_intraday=False, ahplaced='Y',remote_order_id="tag")
```

#### Modifying an order

```py
test_order = Order(order_type='B', scrip_code=1660, quantity=1, price=205,is_intraday=False,exchange='N',exchange_segment='C',exch_order_id="12345678" )
client.modify_order(test_order)
```

#### Canceling an order

```py
client.cancel_order(exchange='N',exchange_segment='C',exch_order_id='12345678')
```
#### Bracket Order 



For placing Braket order
```py
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=205,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=215.0,TriggerPriceForSL=203,LimitPriceForSL=202,ExchType='C',Exch='N',RequestType='P',AtMarket=False)

client.bo_order(test_order)
```
Note:For placing Bracket order in FNO segment pass ExchType='D'

For Modifying Bracket Order only for Initial order (entry)
```py
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=203,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=208.0,TriggerPriceForSL=202,LimitPriceForSL=201,ExchType='C',Exch='N',RequestType='M',AtMarket=False,ExchOrderId='12345678')

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
print(client.fetch_market_depth(a))
```
#### Historical Data
```py
#historical_data(<Exchange>,<Exchange Type>,<Scrip Code>,<Time Frame>,<From Data>,<To Date>)

df=client.historical_data('N','C',1660,'15m','2021-05-25','2021-06-16')
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
 - Call Ladder
 - Put Ladder
 - Ladder
```py
#Import strategy package
from py5paisa.strategy import *
```
Note: These single-commands are capable of trading multiple legs of pre-defined strategies.
Like :- Short/Long Straddles and Strangles, Iron Fly and Iron Condor (many more to come)
Please use these at your own risk.
```py
#Create an Object:-
cred={
    "APP_NAME":"YOUR APP_NAME",
    "APP_SOURCE":YOUR APP_SOURCE,
    "USER_ID":"YOUR USER_ID",
    "PASSWORD":"YOUR PASSWORD",
    "USER_KEY":"YOUR USERKEY",
    "ENCRYPTION_KEY":"YOUR ENCRYPTION_KEY"
    }
strategy=strategies(user="random_email@xyz.com", passw="password", dob="YYYYMMDD",cred=cred)
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
#### Trading Ideas
```py
To get actionable buy trades use:-
print(Client.get_buy())


To get list of current trades use:-
print(Client.get_trade())

```

#### TODO
 - Write tests.


#### Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
