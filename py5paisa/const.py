import os
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
