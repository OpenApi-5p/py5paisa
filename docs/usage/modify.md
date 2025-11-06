## Modifying an order

```py
test_order = Order(order_type='B', scrip_code=1660, quantity=1, price=205,is_intraday=False,exchange='N',exchange_segment='C',atmarket=True,exch_order_id="12345678" )
client.modify_order(test_order)
```
