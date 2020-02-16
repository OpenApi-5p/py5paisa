import requests
import os
from conf import user_key, app_name, user_id, password
from const import GENERIC_PAYLOAD, HEADERS
from helpers.auth_helpers import get_cookie, get_client_code


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

    def __init__(self, data_type):
        self.client_code = get_client_code()
        self.data_type = data_type

    def _request(self):
        payload = GENERIC_PAYLOAD
        payload["body"]["ClientCode"] = self.client_code
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
        cookie = get_cookie()
        response = requests.request(
            "POST", url, json=payload, headers=HEADERS, cookies=cookie)
        return response.json()

    def get_data(self):
        return self._request()

# Usage


if __name__ == "__main__":
    user_holdings = UserInfo(data_type=UserDataType.HOLDINGS)
    print(user_holdings.get_data())
