### Usage


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