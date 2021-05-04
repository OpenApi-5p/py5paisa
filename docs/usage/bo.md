#### Bracket Order 


For placing Braket order
```py
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=204,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=208.0,TriggerPriceForSL=202,RequestType='P',AtMarket=False)

client.bo_order(test_order)
```
Note : For cover order just pass LimitPriceProfitOrder equal to Zero.

For Modifying Bracket Order only for Initial order (entry)
```py
test_order=bo_co_order(scrip_code=1660,BuySell='B',Qty=1, LimitPriceInitialOrder=203,TriggerPriceInitialOrder=0,LimitPriceProfitOrder=208.0,TriggerPriceForSL=202,RequestType='M',AtMarket=False,ExchOrderId='12345678')

client.bo_order(test_order)


```
For Modifying LimitPriceProfitOrder 
```py
test_order=Order(order_type='S', scrip_code=1660, quantity=1, price=208.50,is_intraday=True,exchange='N',exchange_segment='C',atmarket=False,exch_order_id="12345678" ,order_for=OrderFor.MODIFY)

client.mod_bo_order(test_order)
```
For Modifying TriggerPriceForSL
```py
test_order=Order(order_type='S', scrip_code=1660, quantity=1, price=0,is_intraday=True,exchange='N',exchange_segment='C',atmarket=True,exch_order_id="123456789" ,stoploss_price=201.50,is_stoploss_order=True,order_for=OrderFor.MODIFY)

client.mod_bo_order(test_order)

#Note : You have pass atmarket=true while modifying stoploss price, Pass ExchorderId for the particular leg to modify.
```
