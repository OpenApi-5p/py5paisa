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
            "ExchType": "C",
            "ScripCode": 20374,
            "RemoteOrderID": "90980441"
        }]
# Fetches the order status
client.fetch_order_status(req_list_)
```