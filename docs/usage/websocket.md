### Web Socket

####For Subscribe ScripCode

```py

req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":1660},
            
            ]

dict1=client.Request_Feed('mf','s',req_list)


```

####For Subscribe Multiple ScripCode

```py

req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":1660},
            { "Exch":"N","ExchType":"D","ScripCode":61211}
            ]

dict1=client.Request_Feed('mf','s',req_list)

```

####For Unsubscibe ScripCode

```py

req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":1660}
            ]

dict1=client.Request_Feed('mf','u',req_list)

```

####For Unsubscibe Multiple ScripCode

```py

req_list=[
            { "Exch":"N","ExchType":"C","ScripCode":1660},
            { "Exch":"N","ExchType":"D","ScripCode":61211}
            ]

dict1=client.Request_Feed('mf','u',req_list)

```

####Start Streaming

```py
client.Streming_data(dict1)

# Note : Pass Dictionary in Parameter Field
```