from const import GENERIC_PAYLOAD, HEADERS
import requests


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


class OrderFor:

    PLACE = "P"
    MODIFY = "M"
    CANCEL = "C"


# class FullOrder:

#     def __init__(self, order_for=OrderFor.PLACE, exchange=Exchange.NSE, exchange_type=ExchangeType.CASH, price=0.0,
#                  order_id: int, order_type: str, quantity: int, timestamp: str,
#                  scrip_code: int, atmarket=True, remote_order_id: int, exch_order_id: int, disqty: int,
#                  stoploss_price: float, is_stoploss_order=False, ioc_order=False, is_intraday=False, vtd: str,
#                  ahplaced: str, public_ip="", order_validity: int, traded_qty=0, requester_code: int, app_source: int):
#         pass


class Order:

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

    def add_order(self, order: Order) -> None:
        """
        Adds order to the RequestList object required in the request payload.
        """
        self.orders.append(order.__repr__())


class OrderClient(RequestList):

    ORDER_PLACEMENT_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/OrderRequest"
    ORDER_STATUS_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/OrderStatus"
    TRADE_INFO_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/TradeInformation"

    def __init__(self, client_code: str, req_type: str) -> None:

        self.client_code = client_code
        self.req_type = req_type
        self.payload = GENERIC_PAYLOAD

    def _request(self):

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
        print(self.payload)
        res = requests.post(url, json=self.payload, headers=HEADERS)
        print(res.content)

    def fetch_order_status(self, req_list: RequestList) -> None:
        self.payload["OrdStatusReqList"] = req_list.orders
        self._request()

    def fetch_trade_info(self, req_list: RequestList) -> None:
        self.payload["TradeDetailList"] = req_list.orders
        self._request()


"""
Order Status Usage:

order_client = OrderClient(client_code="54059978",
                           req_type=RequestType.ORDER_STATUS)

ITC_order = Order(exchange=Exchange.BSE, exchange_type=ExchangeType.CASH,
                  scrip_code=500875, order_id="90980441")

req_list = RequestList()

req_list.add_order(ITC_order)

order_client.fetch_order_status(req_list)

"""
