### Placing an order

```py
# This is an indicative order.

from py5paisa.order import Order, OrderType, Exchange, ExchangeType

test_order = Order(order_for=OrderType.PLACE, exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, price=0,
            order_id=0, order_type="BUY", quantity=10, scrip_code=500875, atmarket=True, remote_order_id="23324", exch_order_id="0", disqty=10, stoploss_price=0, is_stoploss_order=False, ioc_order=False, is_intraday=False, is_vtd=False, vtd="", ahplaced="Y", public_ip="45.112.149.104", order_validity=0, traded_qty=0)

print(client.place_order(test_order))

```