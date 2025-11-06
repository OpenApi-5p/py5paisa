## Placing an order

```py
from py5paisa.order import Order, OrderType, Exchange

test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code=1660, quantity=1, price=205,is_intraday=True,atmarket=False)
client.place_order(test_order)

```

#### Detailed Usage


#### Placing a stoploss order

By default orders are regular, to place a stoploss order, pass `is_stoploss_order=True` and `stoploss_price` which is the trigger price for your order.

`stoploss_price` is a float and for Buy Stop loss, Trigger price should not be greater than Limit Price. And for Sell Stop Loss Order Trigger Price should not be less than Limit Price.

```py
from py5paisa.order import Order, OrderType
test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code=1660, quantity=1, price=208,is_intraday=True,atmarket=False, is_stoploss_order=True, stoploss_price=207.5)

```

#### Placing offline orders

By default all orders are normal orders, pass `ahplaced=AHPlaced.AFTER_MARKET_CLOSED` to place offline orders.

```py
from py5paisa.order import Order, OrderType, AHPlaced
test_order = Order(order_type='B',exchange='N',exchange_segment='C', scrip_code=1660, quantity=1, price=205,is_intraday=False,atmarket=False, ahplaced=AHPlaced.AFTER_MARKET_CLOSED)

```

#### Enums

Following are the enums which can be imported and used for placing more complex orders.


```py
class Exchange(Enum):

    NSE = "N"
    BSE = "B"
    MCX = "M"
```

```py
class ExchangeSegment(Enum):

    CASH = "C"
    DERIVATIVE = "D"
    CURRENCY = "U"
```

```py
class OrderType(Enum):

    BUY = "BUY"
    SELL = "SELL"
```

```py
class OrderValidity(Enum):

    DAY = 0
    GTD = 1
    GTC = 2
    IOC = 3
    EOS = 4
    FOK = 6
```

```py
class AHPlaced(Enum):

    AFTER_MARKET_CLOSED = "Y"
    NORMAL_ORDER = "N"
```

[Source](https://github.com/5paisa/py5paisa/blob/master/py5paisa/order.py)