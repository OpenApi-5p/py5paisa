import requests
from .auth import EncryptionClient
from .const import GENERIC_PAYLOAD, HEADERS
from .order import *
import time


class FivePaisaClient:

    LOGIN_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/LoginRequestMobileNewbyEmail"

    MARGIN_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V3/Margin"
    ORDER_BOOK_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/OrderBook"
    HOLDINGS_ROUTE = "https://openapi.5paisa.com/VendorsAPI/Service1.svc/V2/Holding"
    POSITIONS_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/NetPositionNetWise"

    ORDER_PLACEMENT_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/OrderRequest"
    ORDER_STATUS_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/OrderStatus"
    TRADE_INFO_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/TradeInformation"

    MARGIN_REQUEST_CODE = "5PMarginV3"
    ORDER_BOOK_REQUEST_CODE = "5POrdBkV2"
    HOLDINGS_REQUEST_CODE = "5PHoldingV2"
    POSITIONS_REQUEST_CODE = "5PNPNWV1"

    def __init__(self, email=None, passwd=None, dob=None):
        """
        Main constructor for client.
        Expects user's email, password and date of birth in YYYYMMDD format.
        """
        self.email = email
        self.passwd = passwd
        self.dob = dob
        self.payload = GENERIC_PAYLOAD
        self.client_code = None
        self.session = requests.Session()

    def login(self):
        encryption_client = EncryptionClient()
        secret_email = encryption_client.encrypt(self.email)
        secret_passwd = encryption_client.encrypt(self.passwd)
        secret_dob = encryption_client.encrypt(self.dob)
        self.payload["body"]["Email_id"] = secret_email
        self.payload["body"]["Password"] = secret_passwd
        self.payload["body"]["My2PIN"] = secret_dob
        self.payload["head"]["requestCode"] = "5PLoginV2"
        res = self._login_request(self.LOGIN_ROUTE)
        self._set_client_code(res["body"]["ClientCode"])
        return self.client_code

    def holdings(self):
        return self._user_info_request("HOLDINGS")

    def margin(self):
        return self._user_info_request("MARGIN")

    def order_book(self):
        return self._user_info_request("ORDER_BOOK")

    def positions(self):
        return self._user_info_request("POSITIONS")

    def _login_request(self, route):
        res = self.session.post(route, json=self.payload, headers=HEADERS)
        return res.json()

    def _set_client_code(self, client_code):
        self.client_code = client_code

    def _user_info_request(self, data_type):
        payload = GENERIC_PAYLOAD
        payload["body"]["ClientCode"] = self.client_code
        if data_type == "MARGIN":
            request_code = self.MARGIN_REQUEST_CODE
            url = self.MARGIN_ROUTE
        elif data_type == "ORDER_BOOK":
            request_code = self.ORDER_BOOK_REQUEST_CODE
            url = self.ORDER_BOOK_ROUTE
        elif data_type == "HOLDINGS":
            request_code = self.HOLDINGS_REQUEST_CODE
            url = self.HOLDINGS_ROUTE
        elif data_type == "POSITIONS":
            request_code = self.POSITIONS_REQUEST_CODE
            url = self.POSITIONS_ROUTE
        else:
            raise Exception("Invalid data type requested")

        payload["head"]["requestCode"] = request_code
        response = self.session.post(url, json=payload, headers=HEADERS)
        return response.json()

    def order_request(self, req_type) -> dict:

        self.payload["body"]["ClientCode"] = self.client_code

        if req_type == "OP":
            url = self.ORDER_PLACEMENT_ROUTE
            self.payload["head"]["requestCode"] = "5POrdReq"
        elif req_type == "OS":
            url = self.ORDER_STATUS_ROUTE
            self.payload["head"]["requestCode"] = "5POrdStatus"
        elif req_type == "TI":
            url = self.TRADE_INFO_ROUTE
            self.payload["head"]["requestCode"] = "5PTrdInfo"
        else:
            raise Exception("Invalid request type!")

        res = self.session.post(url, json=self.payload,
                                headers=HEADERS)
        return res.json()

    def fetch_order_status(self, req_list: RequestList) -> dict:
        self.payload["body"]["OrdStatusReqList"] = req_list.orders
        return self.order_request("OS")

    def fetch_trade_info(self, req_list: RequestList) -> dict:
        self.payload["body"]["TradeDetailList"] = req_list.orders
        return self.order_request("TI")

    def place_order(self, order: Order) -> dict:

        self.payload["body"]["OrderFor"] = order.order_for
        self.payload["body"]["Exchange"] = order.exchange
        self.payload["body"]["ExchangeType"] = order.exchange_type
        self.payload["body"]["Price"] = order.price
        self.payload["body"]["OrderID"] = order.order_id
        self.payload["body"]["OrderType"] = order.order_type
        self.payload["body"]["Qty"] = order.quantity
        # Probably UNIX timestamp
        self.payload["body"]["OrderDateTime"] = f"/Date({int(time.time())})/"
        self.payload["body"]["ScripCode"] = order.scrip_code
        self.payload["body"]["AtMarket"] = str(order.atmarket).lower()
        self.payload["body"]["RemoteOrderID"] = order.remote_order_id
        self.payload["body"]["ExchOrderID"] = order.exch_order_id
        self.payload["body"]["DisQty"] = order.disqty
        self.payload["body"]["IsStopLossOrder"] = str(
            order.is_stoploss_order).lower()
        self.payload["body"]["StopLossPrice"] = order.stoploss_price
        self.payload["body"]["IsVTD"] = str(order.is_vtd).lower()
        self.payload["body"]["IOCOrder"] = str(order.ioc_order).lower()
        self.payload["body"]["IsIntraday"] = str(order.is_intraday).lower()
        self.payload["body"]["PublicIP"] = order.public_ip
        self.payload["body"]["AHPlaced"] = order.ahplaced
        # Hardcoded for now
        self.payload["body"]["ValidTillDate"] = f"/Date({int(time.time())})/"
        self.payload["body"]["TradedQty"] = order.traded_qty
        self.payload["body"]["OrderRequesterCode"] = self.client_code
        self.payload["body"]["AppSource"] = app_source
        self.payload["body"]["iOrderValidity"] = order.order_validity
        return self.order_request("OP")


if __name__ == "__main__":

    client = FivePaisaClient(email="xyz@gmail.com",
                             passwd="password", dob="yyyymmdd")
    client.login()

    ITC_order_status = OrderForStatus(
        exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, scrip_code=500875, order_id=0)
    req_list = RequestList()

    req_list.add_order(ITC_order_status)

    print(client.fetch_order_status(req_list))

    ITC_order = Order(order_for=OrderType.PLACE, exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, price=0, order_id=0, order_type="BUY", quantity=10, scrip_code=500875, atmarket=True, remote_order_id="23324", exch_order_id="0",
                      disqty=10, stoploss_price=0, is_stoploss_order=False, ioc_order=False, is_intraday=False, is_vtd=False, vtd="", ahplaced="Y", public_ip="45.112.149.104", order_validity=0, traded_qty=0)

    print(client.place_order(ITC_order))
