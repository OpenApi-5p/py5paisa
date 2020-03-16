# 5paisa Python SDK


> Python SDK for 5paisa APIs natively written in VB .NET

![5paisa logo](images/5-paisa-img.jpg)

#### Features

-   Supports fetching user info including holdings, positions, margin and order book.
-   Supports order placement, modification and cancellation
-   Supports fetching order status and trade information.

### Usage

#### Fetching user info

```py

from py5paisa.user_info import UserInfo

# Fetching current holdings of the user
# Similarly margin, order book and positions can be fetched by just changing the data type.
user_holdings = UserInfo(data_type=UserDataType.HOLDINGS)
print(user_holdings.get_data())

```

#### Placing an order

```py

# This is an indicative order.

from py5paisa.order import OrderClient, Order, RequestType, OrderType, Exchange, ExchangeType

order_client = OrderClient(req_type=RequestType.ORDER_PLACEMENT)
ITC_order = Order(order_for=OrderType.PLACE, exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, price=0,
                order_id=0, order_type="BUY", quantity=10,scrip_code=500875, atmarket=True,
                remote_order_id="23324", exch_order_id="0", disqty=10, stoploss_price=0,
                is_stoploss_order=False, ioc_order=False, is_intraday=False, is_vtd=False,
                vtd="", ahplaced="Y", public_ip="45.112.149.104", order_validity=0, traded_qty=0)

print(order_client.place_order(ITC_order))

```

#### Fetching Order Status and Trade Information

```py

from py5paisa.order import OrderClient, OrderForStatus, RequestType, Exchange, ExchangeType, RequestList

# To get trade information, simply change the Request type.
order_client = OrderClient(req_type=RequestType.ORDER_STATUS)

ITC_order_status = OrderForStatus(exchange=Exchange.BSE, exchange_type=ExchangeType.CASH,
                                    scrip_code=500875, order_id=0)

req_list = RequestList()

# Add multiple orders to the RequestList to know status of multiple orders at once.
req_list.add_order(ITC_order_status)

print(order_client.fetch_trade_info(req_list))

```




#### TODO
 - Handle responses more gracefully.
 - Write tests.
 - Set cookie and clientCode as environment variables post auth/login.
 - Send cookie, and clientCode post authentication/login.


#### Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
