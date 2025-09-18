"""
Contains reusable payloads across requests
"""
import datetime
from enum import Enum

HEADERS = {'Content-Type': 'application/json'}

GENERIC_PAYLOAD = {
    "head": {
    },
    "body": {
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
    'Authorization':''
    }

JWT_PAYLOAD={
    "ClientCode":"",
    "JWTToken":""
    }
SOCKET_DEPTH_PAYLOAD={
            "operation":"",
            "method":"",
            "instruments":""}

class VTT_TYPE(Enum):
    P = 'VTT'
    M = 'MVTT'
    C = 'CVTT'
    G = 'GVTT'
    H = 'HVTT'

SUBSCRIPTION_KEY="c89fab8d895a426d9e00db380b433027"
TODAY_TIMESTAMP = int(datetime.datetime.today().timestamp())
NEXT_DAY_TIMESTAMP = int(
    (datetime.datetime.today()+datetime.timedelta(days=1)).timestamp())
