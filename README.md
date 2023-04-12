# 5paisa Python SDK

Python SDK for 5paisa APIs natively written in VB .NET

![PyPI](https://img.shields.io/pypi/v/py5paisa)
![GitHub Workflow Status (branch)](https://img.shields.io/github/workflow/status/5paisa/py5paisa/Publish%20package/master)

![5paisa logo](./docs/images/5-paisa-img.jpg)

#### Documentation

Read the docs hosted [here](https://www.5paisa.com/developerapi/overview)

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

Get your API keys from https://tradestation.5paisa.com/apidoc

Note:- 

#### Authentication [New Method]
* First get a token by logging in to -> https://dev-openapi.5paisa.com/WebVendorLogin/VLogin/Index?VendorKey=<Your Vendor Key>&ResponseURL=<Redirect URL>
* VendorKey is UesrKey for individuals user. For example - You can use ResponseURL as https://www.5paisa.com/technology/developer-apis
* Pass the token received in the response url after successful login to get an access token (this also sets the token for all the APIs you use). 
* Please note that you need to copy the request token from URL and paste in this code and start the code within 30s.
       
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
client = FivePaisaClient(cred=cred)
client.get_access_token('Your Response Token') #Put the Response Token here.
```
       
#### Authentication [Old Method] [Deprecated]
We have deprecated the existing method which involved the use of login credentials. 
       
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
client = FivePaisaClient(email="youremail@gmail.com", passwd="Password", dob="YYYYMMDD",cred=cred)
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
#### Market Status
```py
print(client.get_market_status())
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

#### Position Conversion

```py
# Convert positions
# client.position_convertion(<Exchange>,<Exchange Type>,<Scrip Name>,<Buy/Sell>,<Qty>,<From Delivery/Intraday>,<From Delivery/Intraday>)
client.position_convertion("N","C","BPCL_EQ","B",5,"D","I")
```

Scrip codes reference:

Note : Use these Links for getting scrip codes

Scrip Master - https://images.5paisa.com/website/scripmaster-csv-format.csv
#### Placing an order

```py
# Note: This is an indicative order.

from py5paisa.order import Order, OrderType, Exchange

#You can pass scripdata either you can pass scripcode also.
# please use price = 0 for market Order
#use IsIntraday= true for intraday orders

#Using Scrip Data :-

#Using Scrip Code :-
client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=260)
#Sample For SL order (for order to be treated as SL order just pass StopLossPrice)
client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=350, IsIntraday=False, StopLossPrice=345)
#Derivative Order
client.place_order(OrderType='B',Exchange='N',ExchangeType='D', ScripCode = 57633, Qty=50, Price=1.5)

Please refer below documentation link for paramaters to be passed in cleint.place_order function
https://www.5paisa.com/developerapi/order-request-place-order

```
#### Placing offline orders (After Market Orders)

By default all orders are normal orders, pass `AHPlaced=Y` to place offline orders.

```py
client.place_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, Price=325, AHPlaced="Y")
```

#### Modifying an order

```py
client.modify_order(ExchOrderID="1100000017861430", Qty=2,Price=261)
```

#### Cancelling an order

```py
client.cancel_order(exch_order_id="1100000017795041")
```
```py
cancel_bulk=[
            {
                "ExchOrderID": "<Exchange Order ID 1>"
            },
            {
                "ExchOrderID": "<Exchange Order ID 2>"
            },
client.cancel_bulk_order(cancel_bulk)
```
#### SquareOffAll Orders

```py
client.squareoff_all()
```

#### Bracket Order 



For placing Braket order
```py
client.bo_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, LimitPrice=330,TargetPrice=345,StopLossPrice=320,LimitPriceForSL=319,TrailingSL=1.5)

```
For placing Cover order
```py
client.cover_order(OrderType='B',Exchange='N',ExchangeType='C', ScripCode = 1660, Qty=1, LimitPrice=330,StopLossPrice=320,LimitPriceForSL=319,TrailingSL=1.5)
```

Note:For placing Bracket order in FNO segment pass ExchType='D'

For Modifying Bracket/Cover Order only for Initial order (entry)
```py

client.modify_bo_order(ExchOrderID="1100000017861430",LimitPrice=330)
client.modify_cover_order(ExchOrderID="1100000017861430",LimitPrice=330)

#Note : For cover order just pass LimitPriceProfitOrder equal to Zero.
```

For Modifying LimitPriceProfitOrder 
```py
client.modify_bo_order(ExchOrderID="1100000017861430",TargetPrice=330)
client.modify_cover_order(ExchOrderID="1100000017861430",TargetPrice=330)
```
For Modifying TriggerPriceForSL
```py

client.modify_bo_order(ExchOrderID="1100000017861430",LimitPriceForSL=330)
client.modify_bo_order(ExchOrderID="1100000017861430",LimitPriceForSL=330)

#Note : You have pass atmarket=true while modifying stoploss price, Pass ExchorderId for the particular leg to modify.
```

#### Basket Orders

```py
# Create a new Basket
client.create_basket("<New Basket Name>")

# Rename existing basket
client.rename_basket("<Modified Basket Name>",<Exisiting Basket ID>)

# Clone existing basket
client.clone_basket(<Exisiting Basket ID>)

# Delete bulk baskets
delete_basket_list=[{"BasketID":"<Exisiting Basket ID>"},{"BasketID":"<Exisiting Basket ID>"}]
client.delete_basket(delete_basket_list)


# Get list of all baskets (Open/Closed)
client.get_basket()

basket_list= [
            {
                "BasketID": "<Exisiting Basket ID>"
            },
            {
                "BasketID": "<Exisiting Basket ID>"
            }
        ]
order_to_basket=Basket_order("N","C",23000,"BUY",1,"1660","I")
client.add_basket_order(order_to_basket,basket_list)

# Get orders in basket
client.get_order_in_basket(<Exisiting Basket ID>)

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
            "RemoteOrderID": "90980441"
        }]
# Fetches the order status
client.fetch_order_status(req_list_)

# Fetch Trade History

print(client.get_trade_history("PASS EXCHANGE ORDER ID"))

```
#### Live Market Feed Streaming

```py
req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":1660},
            ]

req_data=client.Request_Feed('mf','s',req_list)
def on_message(ws, message):
    print(message)


client.connect(req_data)

client.receive_data(on_message)
```
Note: Use the following abbreviations :

Market Feed=mf

Market Depth (upto 5)=md

Indices (Spot Feed) =i

Open Interest=oi

Subscribe= s

Unsubscribe=u

#### Live Market Depth Streaming (Depth 20)

```py
a={
                "method":"subscribe",
                "operation":"20depth",
                "instruments":["NC2885"]
            }
print(client.socket_20_depth(a))
def on_message(ws, message):
    print(message)
client.receive_data(on_message)

Note:- Instruments in payload above is a list(array) in format as <exchange><exchange type><scrip code>
```

#### Full Market Snapshot 
```py
a=[{"Exchange":"N","ExchangeType":"C","ScripCode":"2885"},
   {"Exchange":"N","ExchangeType":"C","ScripCode":"1660"},
   ]
print(client.fetch_market_depth(a))
```

#### Full Market Snapshot(By Symbol)
```py
a=[{"Exchange":"N","ExchangeType":"C","Symbol":"ITC"},
   {"Exchange":"N","ExchangeType":"D","Symbol":"BANKNIFTY 31 Feb 2022 CE 41600.00"},
   ]
print(client.fetch_market_depth_by_symbol(a))
```

#### Option Chain
```py
client.get_expiry("N","NIFTY")
# Returns list of all active expiries

# client.get_option_chain("N","NIFTY",<Pass expiry timestamp from get_expiry response>)
client.get_option_chain("N","NIFTY",1647507600000)
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
--Old approach
strategy=strategies(user="random_email@xyz.com", passw="password", dob="YYYYMMDD",cred=cred)
--New Approach
strategy=strategies(cred=cred,request_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6IjUwMDUyNzcwIiwicm9sZSI6ImdpUUlvYXR5R2NYQUR3eFYwNXVXSGlPVzJRT1dOTGNzIiwibmJmIjoxNjY3ODMwODczLCJleHAiOjE2Njc4MzA5MDMsImlhdCI6MTY2NzgzMDg3M30.iP_FZtFy-nj6QeRd0sEhaKS-jr-wu-pCwtcdYCGPeO4")

```
Use the following to execute the strategy (note:- they are executed at market price only)
```py
#short_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
strategy.short_straddle("banknifty",'37000','50','20210610','I',tag='<Your strategy Name>')

#Using tag is optional
```
```py
#short_strangle(<symbol>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.short_strangle("banknifty",['35300','37000'],'50','20210610','D')
```
```py
#long_straddle(<symbol>,<strike price>,<qty>,<expiry>,<Order Type>)
strategy.long_straddle("banknifty",'37000','50','20210610','I',tag='<Your strategy Name>')

#Using tag is optional
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
strategy.iron_fly("NIFTY",["15000","15200"],"15100","75","20210610","I",tag='<Your strategy Name>')

#Using tag is optional
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
strategy.put_ladder("NIFTY","15000",["14800","14500"],"75","20210610","I",tag='<Your strategy Name>')

#Using tag is optional
```

```py
#ladder(<symbol>,<List of Buy strike prices>,<List of Sell strike price>,<qty>,<expiry>,<Order Type>)
strategy.ladder("sbin",["400","420"],["350","370","450","500"],"1500","20210729","D")
```

```py
Squareoff a strategy Using tags
strategy.squareoff('tag')

# Use the same tag as used while executing the strategies
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
