from conf import app_name, user_id, password, user_key

HEADERS = {'content-type': 'application/json'}

GENERIC_PAYLOAD = {
    "head": {
        "appName": app_name,
        "appVer": "1.0",
        "key": user_key,
        "osName": "WEB",
        "requestCode": "",
        "userId": user_id,
        "password": password
    },
    "body": {
        "ClientCode": ""
    }
}

LOGIN_PAYLOAD = {"head":{
"appName":app_name,
        "appVer": "1.0",
        "key": user_key,
        "osName": "WEB",
        "requestCode": "5PLoginV2",
        "userId": user_id,
        "password": password
},
"body":
{
"Email_id":"",
"Password": "",
"LocalIP": "",
"PublicIP": "",
"HDSerailNumber": "",
"MACAddress": "",
"MachineID": "039377",
"VersionNo": "1.7",
"RequestNo": "1",
"My2PIN": "",
"ConnectionType": "1"
}
}

