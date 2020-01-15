import requests
import os


class UserDataType:

    def __init__(self):
        super().__init__()

    MARGIN = "MARGIN"
    ORDER_BOOK = "ORDER_BOOK"
    HOLDINGS = "HOLDINGS"
    POSITIONS = "POSITIONS"


class UserInfo:

    MARGIN_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V3/Margin"
    ORDER_BOOK_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/OrderBook"
    HOLDINGS_ROUTE = "https://openapi.5paisa.com/VendorsAPI/Service1.svc/V2/Holding"
    POSITIONS_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/NetPositionNetWise"

    MARGIN_REQUEST_CODE = "5PMarginV3"
    ORDER_BOOK_REQUEST_CODE = "5POrdBkV2"
    HOLDINGS_REQUEST_CODE = "5PHoldingV2"
    POSITIONS_REQUEST_CODE = "5PNPNWV1"

    def __init__(self, app_name=None, userid=None, passwd=None, client_code=None, data_type=None):
        self.app_name = app_name
        self.userid = userid
        self.passwd = passwd
        self.client_code = client_code
        self.data_type = data_type
        self.user_key = None

    def get_key(self):
        user_key = os.getenv("USER_KEY")
        if not user_key:
            raise Exception("USER_KEY environment variable not set")
        return user_key

    def _request(self):
        headers = {'content-type': 'application/json'}
        payload = {
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
        self.user_key = self.get_key()
        payload["head"]["appName"] = self.app_name
        payload["head"]["key"] = self.user_key
        payload["body"]["ClientCode"] = self.client_code
        payload["head"]["userId"] = self.userid
        payload["head"]["password"] = self.passwd
        if self.data_type == "MARGIN":
            request_code = self.MARGIN_REQUEST_CODE
            url = self.MARGIN_ROUTE
        elif self.data_type == "ORDER_BOOK":
            request_code = self.ORDER_BOOK_REQUEST_CODE
            url = self.ORDER_BOOK_ROUTE
        elif self.data_type == "HOLDINGS":
            request_code = self.HOLDINGS_REQUEST_CODE
            url = self.HOLDINGS_ROUTE
        elif self.data_type == "POSITIONS":
            request_code = self.POSITIONS_REQUEST_CODE
            url = self.POSITIONS_ROUTE
        else:
            raise Exception("Invalid data type requested")

        payload["head"]["requestCode"] = request_code
        response = requests.request(
            "POST", url, json=payload, headers=headers)
        print(response.text)
        return response.text

    def get_data(self):
        self._request()
