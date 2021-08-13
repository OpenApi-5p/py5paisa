"""
Contains reusable payloads across requests
"""
import datetime

HEADERS = {'Content-Type': 'application/json'}

GENERIC_PAYLOAD = {
    "head": {
        "appName": "",
        "appVer": "1.0",
        "key": "",
        "osName": "WEB",
        "requestCode": "",
        "userId": "",
        "password": ""
    },
    "body": {
        "ClientCode": ""
    }
}
LOGIN_PAYLOAD = {"head": {
    "appName": "",
    "appVer": "1.0",
    "key": "",
    "osName": "WEB",
    "requestCode": "5PLoginV2",
    "userId": "",
    "password": ""
},
    "body":
    {
    "Email_id": "",
    "Password": "",
    "LocalIP": "192.168.10.10",
    "PublicIP": "192.168.10.10",
    "HDSerailNumber": "",
    "MACAddress": "",
    "MachineID": "039377",
    "VersionNo": "1.7",
    "RequestNo": "1",
    "My2PIN": "",
    "ConnectionType": "1"
}
}
LOGIN_CHECK_PAYLOAD={
    "head" : {
        "requestCode":"5PLoginCheck",
        "key":"",
        "appVer":"1.0",
        "appName":"",
        "osName":"WEB",
        "LoginId":""
        },
    "body":{
        "RegistrationID":""
        }
    }
WS_PAYLOAD={"Method":"",
            "Operation":"",
            "ClientCode":"",
            "MarketFeedData":""}

JWT_HEADERS={
    'Ocp-Apim-Subscription-Key': 'c89fab8d895a426d9e00db380b433027',
    'x-clientcode':"",
    'x-auth-token':""
    }

JWT_PAYLOAD={
    "ClientCode":"",
    "JWTToken":""
    }

TODAY_TIMESTAMP = int(datetime.datetime.today().timestamp())
NEXT_DAY_TIMESTAMP = int(
    (datetime.datetime.today()+datetime.timedelta(days=1)).timestamp())
