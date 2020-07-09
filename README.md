# 5paisa Python SDK


> Python SDK for 5paisa APIs natively written in VB .NET

![5paisa logo](images/5-paisa-img.jpg)

#### Features

-   Supports fetching user info including holdings, positions, margin and order book.
-   Supports order placement, modification and cancellation
-   Supports fetching order status and trade information.

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

After successful authentication, the cookie is persisted for subsequent requests.


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

#### Placing an order

```py
# This is an indicative order.

from py5paisa.order import Order, OrderType, Exchange, ExchangeType

test_order = Order(order_for=OrderType.PLACE, exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, price=0,
            order_id=0, order_type="BUY", quantity=10, scrip_code=500875, atmarket=True, remote_order_id="23324", exch_order_id="0", disqty=10, stoploss_price=0, is_stoploss_order=False, ioc_order=False, is_intraday=False, is_vtd=False, vtd="", ahplaced="Y", public_ip="45.112.149.104", order_validity=0, traded_qty=0)

print(client.place_order(test_order))

```

#### Fetching Order Status and Trade Information

```py
from py5paisa.order import OrderForStatus, Exchange, ExchangeType, RequestList

test_order_status = OrderForStatus(exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, scrip_code=500875, order_id=0)

req_list = RequestList()
# Add multiple orders to the RequestList to know status of multiple orders at once.
req_list.add_order(test_order_status)

# Fetches the trade details
print(client.fetch_trade_info(req_list))

# Fetches the order status
print(client.fetch_order_status(req_list))

```

#### TODO
 - Handle responses more gracefully.
 - Write tests.
 - Add logging


#### Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
