#### Market Feed

```py
# NOTE : Symbol has to be in the same format as specified in the example below.

req_list_=[{"Exch":"N","ExchType":"D","Symbol":"NIFTY 22 APR 2021 CE 15200.00","Expiry":"20210422","StrikePrice":"15200","OptionType":"CE"},
            {"Exch":"N","ExchType":"D","Symbol":"NIFTY 22 APR 2021 PE 15200.00","Expiry":"20210422","StrikePrice":"15200","OptionType":"PE"}]
            
client.fetch_market_feed(req_list_)
```
