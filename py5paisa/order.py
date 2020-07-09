"""
Contains base classes for Orders etc.
"""
from .const import GENERIC_PAYLOAD, HEADERS
import requests
from .conf import APP_SOURCE


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
        self.app_source = int(APP_SOURCE)


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
