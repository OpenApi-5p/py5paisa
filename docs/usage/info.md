### Information

#### User information

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


#### Order Status and Trade Information

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