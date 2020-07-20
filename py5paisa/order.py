"""
Contains base classes for Orders etc.
"""
from .const import GENERIC_PAYLOAD, HEADERS, NEXT_DAY_TIMESTAMP
import requests
from .conf import APP_SOURCE
from enum import Enum


class Exchange(Enum):

    NSE = "N"
    BSE = "B"
    MCX = "M"


class ExchangeSegment(Enum):

    CASH = "C"
    DERIVATIVE = "D"
    CURRENCY = "U"


class OrderFor(Enum):

    PLACE = "P"
    MODIFY = "M"
    CANCEL = "C"


class OrderType(Enum):

    BUY = "BUY"
    SELL = "SELL"


class OrderValidity(Enum):

    DAY = 0
    GTD = 1
    GTC = 2
    IOC = 3
    EOS = 4
    FOK = 6


class AHPlaced(Enum):

    AFTER_MARKET_CLOSED = "Y"
    NORMAL_ORDER = "N"


class Order:

    def __init__(self, order_type: OrderType, scrip_code: int, quantity: int, order_for: OrderFor = OrderFor.PLACE, exchange: Exchange = Exchange.BSE,
                 exchange_segment: ExchangeSegment = ExchangeSegment.CASH, price: float = 0.0, order_id: int = 0,
                 atmarket: bool = True, remote_order_id: int = 1, exch_order_id: int = 0,
                 stoploss_price: float = 0, is_stoploss_order: bool = False, ioc_order: bool = False,
                 is_intraday: bool = False, is_vtd: bool = False, vtd: str = f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced: AHPlaced = AHPlaced.NORMAL_ORDER, public_ip: str = '192.168.1.1',
                 order_validity: OrderValidity = OrderValidity.DAY, traded_qty: int = 0):

        self.order_for = order_for.value
        self.exchange = exchange.value
        self.exchange_segment = exchange_segment.value
        self.price = price
        self.order_id = order_id
        self.order_type = order_type.value
        self.quantity = quantity
        self.scrip_code = scrip_code
        self.atmarket = atmarket
        self.remote_order_id = remote_order_id
        self.exch_order_id = exch_order_id
        self.disqty = quantity
        self.stoploss_price = stoploss_price
        self.is_stoploss_order = is_stoploss_order
        self.ioc_order = ioc_order
        self.is_intraday = is_intraday
        self.is_vtd = is_vtd
        self.vtd = vtd
        self.ahplaced = ahplaced.value
        self.public_ip = public_ip
        self.order_validity = order_validity.value
        self.traded_qty = traded_qty
        self.app_source = int(APP_SOURCE)


class OrderForStatus:
    """
    Order class for representing an order for only Status and trade information request.
    """

    def __init__(self, exchange: Exchange, exchange_segment: ExchangeSegment, scrip_code: int, order_id: str) -> None:
        self.exchange = exchange
        self.exchange_segment = exchange_segment
        self.scrip_code = scrip_code
        self.order_id = order_id

    def __str__(self):
        return f"Order -> Exchange:{self.exchange}, Type: {self.exchange_segment}, Scrip Code: {self.scrip_code}, Order ID: {self.order_id}"

    def __repr__(self) -> dict:
        """
        Overriding repr to return dict which can be directly appended to the orders list.
        """
        return {
            "Exch": self.exchange,
            "ExchSegment": self.exchange_segment,
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
