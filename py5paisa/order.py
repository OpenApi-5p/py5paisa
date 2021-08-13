"""
Contains base classes for Orders etc.
"""
from .const import GENERIC_PAYLOAD, HEADERS, NEXT_DAY_TIMESTAMP
import requests
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

    def __init__(self, order_type: str, scrip_code: int, quantity: int, exchange: str,
                 exchange_segment: str, price: float ,is_intraday: bool , atmarket: bool ,order_id: int = 0,
                  remote_order_id: int = 1, exch_order_id: int = 0, order_for: str = 'P',
                 stoploss_price: float = 0, is_stoploss_order: bool = False, ioc_order: bool = False,
                  is_vtd: bool = False, vtd: str = f"/Date({NEXT_DAY_TIMESTAMP})/",
                 ahplaced: str= 'N', public_ip: str = '192.168.1.1',
                 order_validity: int =0, traded_qty: int = 0):

        self.order_for = order_for
        self.exchange = exchange
        self.exchange_segment = exchange_segment
        self.price = price
        self.order_id = order_id
        self.order_type = order_type
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
        self.ahplaced = ahplaced
        self.public_ip = public_ip
        self.order_validity = order_validity
        self.traded_qty = traded_qty
        

class bo_co_order:

    def __init__(self,scrip_code: int, Qty: int,LimitPriceInitialOrder:float,TriggerPriceInitialOrder:float
                 ,LimitPriceProfitOrder:float,BuySell:str,Exch: str,ExchType:  str,RequestType: str,
                 TriggerPriceForSL:float,TrailingSL:int=0,StopLoss:int=0,
                 LocalOrderIDNormal:int=0,LocalOrderIDSL:int=0,LocalOrderIDLimit:int=0,
                 public_ip: str = '192.168.1.1',traded_qty: int = 0,
                 order_for: str="S",
                 DisQty: int=0,ExchOrderId:str="0",AtMarket: bool = False,UniqueOrderIDNormal:str="",
                 UniqueOrderIDSL:str="",UniqueOrderIDLimit:str=""):
        

        self.order_for = order_for
        self.Exch = Exch
        self.ExchType = ExchType
        self.RequestType=RequestType
        self.BuySell=BuySell
        self.scrip_code=scrip_code
        self.DisQty=DisQty
        self.LimitPriceInitialOrder=LimitPriceInitialOrder
        self.TriggerPriceInitialOrder=TriggerPriceInitialOrder
        self.LimitPriceProfitOrder=LimitPriceProfitOrder
        self.AtMarket=AtMarket
        self.TriggerPriceForSL=TriggerPriceForSL
        self.TrailingSL=TrailingSL
        self.StopLoss=StopLoss
        self.UniqueOrderIDNormal=UniqueOrderIDNormal
        self.UniqueOrderIDSL=UniqueOrderIDSL
        self.UniqueOrderIDLimit=UniqueOrderIDLimit
        self.LocalOrderIDNormal=LocalOrderIDNormal
        self.LocalOrderIDSL=LocalOrderIDSL
        self.LocalOrderIDLimit=LocalOrderIDLimit
        self.public_ip=public_ip
        self.ExchOrderId=ExchOrderId
        self.traded_qty =traded_qty
        self.Qty=Qty
        
        if LimitPriceProfitOrder==0:
            self.order_for="C"

