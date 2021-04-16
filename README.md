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
-   Fetching order status and trade information.

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

BSE: https://www.bseindia.com/
NSE: https://nse-scrips.herokuapp.com/

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

#### Fetching Order Status and Trade Information

```py
from py5paisa.order import OrderForStatus, Exchange, ExchangeType, RequestList

test_order_status = OrderForStatus(exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, scrip_code=500875, order_id=0)

req_list = RequestList()
# Add multiple orders to the RequestList to know status of multiple orders at once.
req_list.add_order(test_order_status)

# Fetches the trade details
client.fetch_trade_info(req_list)

# Fetches the order status
client.fetch_order_status(req_list)

```

#### TODO
 - Write tests.


#### Credits

This package was created with
[Cookiecutter](https://github.com/audreyr/cookiecutter) and the
[audreyr/cookiecutter-pypackage](https://github.com/audreyr/cookiecutter-pypackage)
project template.
