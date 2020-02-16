from const import GENERIC_PAYLOAD, HEADERS
import requests
from helpers.auth_helpers import get_cookie, get_client_code
import time
from conf import app_source


class RequestType:

    ORDER_PLACEMENT = "OP"
    ORDER_STATUS = "OS"
    TRADE_INFO = "TI"


class Exchange:

    NSE = "N"
    BSE = "B"
    MCX = "M"


class ExchangeType:

    CASH = "C"
    DERIVATIVE = "D"
    CURRENCY = "U"


class OrderType:

    PLACE = "P"
    MODIFY = "M"
    CANCEL = "C"


class Order:

    def __init__(self, order_for: str, exchange: str, exchange_type: str, price: float,
                 order_id: int, order_type: str, quantity: int,
                 scrip_code: int, atmarket: bool, remote_order_id: int, exch_order_id: int, disqty: int,
                 stoploss_price: float, is_stoploss_order: bool, ioc_order: bool, is_intraday: bool, is_vtd: bool, vtd: str,
                 ahplaced: str, public_ip: str, order_validity: int, traded_qty: int):

        self.order_for = order_for
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.price = price
        self.order_id = order_id
        self.order_type = order_type
        self.quantity = quantity
        self.scrip_code = scrip_code
        self.atmarket = atmarket
        self.remote_order_id = remote_order_id
        self.exch_order_id = exch_order_id
        self.disqty = disqty
        self.stoploss_price = stoploss_price
        self.is_stoploss_order = is_stoploss_order
        self.ioc_order = ioc_order
        self.is_intraday = is_intraday
        self.is_vtd = is_vtd
        self.vtd = vtd
        self.ahplaced = ahplaced
        self.public_ip = public_ip
        self.order_validity = order_validity
        self.traded_qty = traded_qty
        self.requester_code = get_client_code()
        self.app_source = int(app_source)


class OrderForStatus:
    """
    Order class for representing an order for only Status and trade information request.
    """

    def __init__(self, exchange: str, exchange_type: str, scrip_code: int, order_id: str) -> None:
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.scrip_code = scrip_code
        self.order_id = order_id

    def __str__(self):
        return f"Order -> Exchange:{self.exchange}, Type: {self.exchange_type}, Scrip Code: {self.scrip_code}, Order ID: {self.order_id}"

    def __repr__(self) -> dict:
        """
        Overriding repr to return dict which can be directly appended to the orders list.
        """
        return {
            "Exch": self.exchange,
            "ExchType": self.exchange_type,
            "ScripCode": self.scrip_code,
            "RemoteOrderID": self.order_id
        }


class RequestList:

    def __init__(self):
        self.orders = []

    def add_order(self, order: OrderForStatus) -> None:
        """
        Adds order to the RequestList object required in the request payload.
        """
        self.orders.append(order.__repr__())


class OrderClient(RequestList):

    ORDER_PLACEMENT_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/OrderRequest"
    ORDER_STATUS_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/OrderStatus"
    TRADE_INFO_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/TradeInformation"

    def __init__(self, req_type: str) -> None:

        self.client_code = get_client_code()
        print(self.client_code)
        self.req_type = req_type
        self.payload = GENERIC_PAYLOAD

    def _request(self) -> dict:

        self.payload["body"]["ClientCode"] = self.client_code

        if self.req_type == "OP":
            url = self.ORDER_PLACEMENT_ROUTE
            self.payload["head"]["requestCode"] = "5POrdReq"
        elif self.req_type == "OS":
            url = self.ORDER_STATUS_ROUTE
            self.payload["head"]["requestCode"] = "5POrdStatus"
        elif self.req_type == "TI":
            url = self.TRADE_INFO_ROUTE
            self.payload["head"]["requestCode"] = "5PTrdInfo"
        else:
            raise Exception("Invalid request type!")
        cookie = get_cookie()
        res = requests.post(url, json=self.payload,
                            headers=HEADERS, cookies=cookie)
        return res.content

    def fetch_order_status(self, req_list: RequestList) -> dict:
        self.payload["body"]["OrdStatusReqList"] = req_list.orders
        return self._request()

    def fetch_trade_info(self, req_list: RequestList) -> dict:
        self.payload["body"]["TradeDetailList"] = req_list.orders
        return self._request()

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
        self.payload["body"]["OrderRequesterCode"] = order.requester_code
        self.payload["body"]["AppSource"] = app_source
        self.payload["body"]["iOrderValidity"] = order.order_validity
        return self._request()


# Usage
if __name__ == "__main__":

    order_client = OrderClient(req_type=RequestType.ORDER_STATUS)

    ITC_order_status = OrderForStatus(exchange=Exchange.BSE, exchange_type=ExchangeType.CASH,
                                      scrip_code=500875, order_id=0)

    req_list = RequestList()

    req_list.add_order(ITC_order_status)

    print(order_client.fetch_trade_info(req_list))

    order_client = OrderClient(req_type=RequestType.ORDER_PLACEMENT)
    ITC_order = Order(order_for=OrderType.PLACE, exchange=Exchange.BSE, exchange_type=ExchangeType.CASH, price=0, order_id=0, order_type="BUY", quantity=10, scrip_code=500875, atmarket=True, remote_order_id="23324", exch_order_id="0",
                      disqty=10, stoploss_price=0, is_stoploss_order=False, ioc_order=False, is_intraday=False, is_vtd=False, vtd="", ahplaced="Y", public_ip="45.112.149.104", order_validity=0, traded_qty=0)

    print(order_client.place_order(ITC_order))
