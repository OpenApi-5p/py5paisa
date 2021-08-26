import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .auth import EncryptionClient
from .const import GENERIC_PAYLOAD, LOGIN_PAYLOAD, HEADERS, NEXT_DAY_TIMESTAMP, TODAY_TIMESTAMP,LOGIN_CHECK_PAYLOAD,WS_PAYLOAD,JWT_PAYLOAD,JWT_HEADERS
from .order import Order, bo_co_order, OrderType, OrderFor
from .logging import log_response
import datetime
from typing import Union
import json
import websocket
import pandas as pd

class FivePaisaClient:

    LOGIN_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V3/LoginRequestMobileNewbyEmail"

    MARGIN_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V3/Margin"
    ORDER_BOOK_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V2/OrderBook"
    HOLDINGS_ROUTE = "https://openapi.5paisa.com/VendorsAPI/Service1.svc/V2/Holding"
    POSITIONS_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/NetPositionNetWise"

    ORDER_PLACEMENT_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/OrderRequest"
    ORDER_STATUS_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/OrderStatus"
    TRADE_INFO_ROUTE = "https://Openapi.5paisa.com/VendorsAPI/Service1.svc/TradeInformation"
    
    BRACKET_MOD_ROUTE="https://openapi.5paisa.com/VendorsAPI/Service1.svc/ModifySMOOrder"
    BRACKET_ORDER_ROUTE="https://openapi.5paisa.com/VendorsAPI/Service1.svc/SMOOrderRequest"
    
    MARKET_FEED_ROUTE="https://Openapi.5paisa.com/VendorsAPI/Service1.svc/MarketFeed"
    LOGIN_CHECK_ROUTE="https://openfeed.5paisa.com/Feeds/api/UserActivity/LoginCheck"

    MARKET_DEPTH_ROUTE="https://openapi.5paisa.com/VendorsAPI/Service1.svc/MarketDepth"
    JWT_VALIDATION_ROUTE="https://Openapi.indiainfoline.com/VendorsAPI/Service1.svc/JWTOpenApiValidation"
    HISTORICAL_DATA_ROUTE="https://openapi.5paisa.com/historical/"

    IDEAS_ROUTE="https://openapi.5paisa.com/VendorsAPI/Service1.svc/TraderIDEAs"

    TRADEBOOK_ROUTE="https://Openapi.5paisa.com/VendorsAPI/Service1.svc/V1/TradeBook"
    
    MARGIN_REQUEST_CODE = "5PMarginV3"
    ORDER_BOOK_REQUEST_CODE = "5POrdBkV2"
    HOLDINGS_REQUEST_CODE = "5PHoldingV2"
    POSITIONS_REQUEST_CODE = "5PNPNWV1"
    IDEAS_REQUEST_CODE ="5PTraderIDEAs"


   

    def __init__(self, email=None, passwd=None, dob=None,cred=None):
        """
        Main constructor for client.
        Expects user's email, password and date of birth in YYYYMMDD format.
        """
        self.email = email
        self.passwd = passwd
        self.dob = dob
        self.payload = GENERIC_PAYLOAD
        self.login_payload = LOGIN_PAYLOAD
        self.login_check_payload= LOGIN_CHECK_PAYLOAD
        self.ws_payload=WS_PAYLOAD
        self.jwt_headers=JWT_HEADERS
        self.jwt_payload=JWT_PAYLOAD
        self.client_code = None
        self.Jwt_token = None
        self.Aspx_auth = None
        self.web_url= None
        self.session = requests.Session()
        self.APP_SOURCE=cred["APP_SOURCE"]
        self.APP_NAME=cred["APP_NAME"]
        self.USER_ID=cred["USER_ID"]
        self.PASSWORD=cred["PASSWORD"]
        self.USER_KEY=cred["USER_KEY"]
        self.ENCRYPTION_KEY=cred["ENCRYPTION_KEY"]
        
        

    def login(self):
        encryption_client = EncryptionClient(self.ENCRYPTION_KEY)
        secret_email = encryption_client.encrypt(self.email)
        secret_passwd = encryption_client.encrypt(self.passwd)
        secret_dob = encryption_client.encrypt(self.dob)
        self.login_payload["body"]["Email_id"] = secret_email
        self.login_payload["body"]["Password"] = secret_passwd
        self.login_payload["body"]["My2PIN"] = secret_dob
        self.login_payload["head"]["requestCode"] = "5PLoginV3"
        self.login_payload["head"]["appName"] = self.APP_NAME
        self.login_payload["head"]["key"] = self.USER_KEY
        self.login_payload["head"]["userId"] = self.USER_ID
        self.login_payload["head"]["password"] = self.PASSWORD  
        res = self._login_request(self.LOGIN_ROUTE)
        message = res["body"]["Message"]
        if message == "":
            log_response("Logged in!!")
        else:
            log_response(message)
        self._set_client_code(res["body"]["ClientCode"])

    def holdings(self):
        return self._user_info_request("HOLDINGS")

    def margin(self):
        return self._user_info_request("MARGIN")

    def order_book(self):
        return self._user_info_request("ORDER_BOOK")

    def positions(self):
        return self._user_info_request("POSITIONS")

    def _login_request(self, route):
        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
        res = self.session.post(route, json=self.login_payload, headers=HEADERS)
        
        session_cookies = res.cookies
        
        cookies_dictionary = session_cookies.get_dict()
        self.Jwt_token=cookies_dictionary['JwtToken']
        
        
        return res.json()

    def _set_client_code(self, client_code):
        self.client_code = client_code

    def _user_info_request(self, data_type):
        payload = GENERIC_PAYLOAD
        payload["head"]["appName"] = self.APP_NAME
        payload["head"]["key"] = self.USER_KEY
        payload["head"]["userId"] = self.USER_ID
        payload["head"]["password"] = self.PASSWORD
        payload["body"]["ClientCode"] = self.client_code
        return_type = ""
        if data_type == "MARGIN":
            request_code = self.MARGIN_REQUEST_CODE
            url = self.MARGIN_ROUTE
            return_type = "EquityMargin"
        elif data_type == "ORDER_BOOK":
            request_code = self.ORDER_BOOK_REQUEST_CODE
            url = self.ORDER_BOOK_ROUTE
            return_type = "OrderBookDetail"
        elif data_type == "HOLDINGS":
            request_code = self.HOLDINGS_REQUEST_CODE
            url = self.HOLDINGS_ROUTE
            return_type = "Data"
        elif data_type == "POSITIONS":
            request_code = self.POSITIONS_REQUEST_CODE
            url = self.POSITIONS_ROUTE
            return_type = "NetPositionDetail"
        elif data_type == "IB":
            url = self.IDEAS_ROUTE
            request_code = self.IDEAS_REQUEST_CODE
            return_type = "Data"
        elif data_type == "IT":
            url = self.IDEAS_ROUTE
            request_code = self.IDEAS_REQUEST_CODE
            return_type = "Data"
        else:
            raise Exception("Invalid data type requested")

        payload["head"]["requestCode"] = request_code
        response = self.session.post(url, json=payload, headers=HEADERS).json()
        message = response["body"]["Message"]
        data = response["body"][return_type]
        return data

    def order_request(self, req_type) -> None:

        self.payload["body"]["ClientCode"] = self.client_code
        self.payload["head"]["appName"] = self.APP_NAME
        self.payload["head"]["key"] = self.USER_KEY
        self.payload["head"]["userId"] = self.USER_ID
        self.payload["head"]["password"] = self.PASSWORD 
        if req_type == "OP":
            url = self.ORDER_PLACEMENT_ROUTE
            self.payload["head"]["requestCode"] = "5POrdReq"
        elif req_type == "OS":
            url = self.ORDER_STATUS_ROUTE
            self.payload["head"]["requestCode"] = "5POrdStatus"
        elif req_type == "TI":
            url = self.TRADE_INFO_ROUTE
            self.payload["head"]["requestCode"] = "5PTrdInfo"
        elif req_type == "MF":
            url = self.MARKET_FEED_ROUTE
            self.payload["head"]["requestCode"] = "5PMF"
            self.payload["body"]["COUNT"]=self.client_code
        elif req_type == "BM":
            url = self.BRACKET_MOD_ROUTE
            self.payload["head"]["requestCode"] = "5PSModMOOrd"
            self.payload["body"]["legtype"]=0
            self.payload["body"]["TMOPartnerOrderID"]=0
        elif req_type == "BO":
            url = self.BRACKET_ORDER_ROUTE
            self.payload["head"]["requestCode"] = "5PSMOOrd"
            self.payload["body"]["OrderRequesterCode"]=self.client_code
        elif req_type == "MD":
            url = self.MARKET_DEPTH_ROUTE
            self.payload["head"]["requestCode"] = "5PMD"
        elif req_type == "TB":
            url = self.TRADEBOOK_ROUTE
            self.payload["head"]["requestCode"] = "5PTrdBkV1"
        
            
        else:
            raise Exception("Invalid request type!")

        
        res = self.session.post(url, json=self.payload,
                                headers=HEADERS).json()
        log_response(res["body"]["Message"])
        return res["body"]

    def fetch_order_status(self, req_list:list) :
        self.payload["body"]["OrdStatusReqList"] = req_list
        return self.order_request("OS")

    def fetch_trade_info(self, req_list:list) :
        self.payload["body"]["TradeInformationList"] = req_list
        return self.order_request("TI")

    def fetch_market_depth(self, req_list:list):
        self.payload["body"]["Count"]="1"
        self.payload["body"]["Data"]=req_list
        
        return self.order_request("MD")
        
    
    def fetch_market_feed(self, req_list:list) :
        """
            market feed api
        """
        
        self.payload["body"]["MarketFeedData"] = req_list
        self.payload["body"]["ClientLoginType"] = 0
        self.payload["body"]["LastRequestTime"] = f"/Date({TODAY_TIMESTAMP})/"
        self.payload["body"]["RefreshRate"] = "H"
        return self.order_request("MF")

    def set_payload(self, order: Order) -> None:
        self.payload["head"]["appName"] = self.APP_NAME
        self.payload["head"]["key"] = self.USER_KEY
        self.payload["head"]["userId"] = self.USER_ID
        self.payload["head"]["password"] = self.PASSWORD 
        self.payload["body"]["OrderFor"] = order.order_for
        self.payload["body"]["Exchange"] = order.exchange
        self.payload["body"]["ExchangeType"] = order.exchange_segment
        self.payload["body"]["Price"] = order.price
        self.payload["body"]["OrderID"] = order.order_id
        self.payload["body"]["OrderType"] = order.order_type
        self.payload["body"]["Qty"] = order.quantity
        # Passing today's unix timestamp
        self.payload["body"]["OrderDateTime"] = f"/Date({TODAY_TIMESTAMP})/"
        self.payload["body"]["ScripCode"] = order.scrip_code
        self.payload["body"]["AtMarket"] = str(order.atmarket).lower()
        self.payload["body"]["RemoteOrderID"] = order.remote_order_id
        self.payload["body"]["ExchOrderID"] = order.exch_order_id
        self.payload["body"]["DisQty"] = order.disqty
        self.payload["body"]["IsStopLossOrder"] = str(
            order.is_stoploss_order).lower()
        self.payload["body"]["IsVTD"] = str(order.is_vtd).lower()
        self.payload["body"]["IOCOrder"] = str(order.ioc_order).lower()
        self.payload["body"]["IsIntraday"] = str(order.is_intraday).lower()
        self.payload["body"]["PublicIP"] = order.public_ip
        self.payload["body"]["AHPlaced"] = order.ahplaced
        # Passing the next day's UNIX timestamp
        self.payload["body"]["ValidTillDate"] = f"/Date({NEXT_DAY_TIMESTAMP})/"
        self.payload["body"]["TradedQty"] = order.traded_qty
        self.payload["body"]["OrderRequesterCode"] = self.client_code
        self.payload["body"]["AppSource"] = self.APP_SOURCE
        self.payload["body"]["iOrderValidity"] = order.order_validity
        
    def set_payload_bo(self,boco:bo_co_order)-> None:
        """
            this is for bo-co order placement
        """
        
        self.payload["head"]["appName"] = self.APP_NAME
        self.payload["head"]["key"] = self.USER_KEY
        self.payload["head"]["userId"] = self.USER_ID
        self.payload["head"]["password"] = self.PASSWORD 
        self.payload["body"]["RequestType"] = boco.RequestType
        self.payload["body"]["BuySell"] = boco.BuySell
        self.payload["body"]["Qty"] = boco.Qty
        self.payload["body"]["Exch"] = boco.Exch
        self.payload["body"]["ExchType"] = boco.ExchType
        self.payload["body"]["DisQty"] = boco.DisQty
        self.payload["body"]["AtMarket"] = boco.AtMarket
        self.payload["body"]["ExchOrderId"] = boco.ExchOrderId
        self.payload["body"]["LimitPriceInitialOrder"] = boco.LimitPriceInitialOrder
        self.payload["body"]["TriggerPriceInitialOrder"] = boco.TriggerPriceInitialOrder
        self.payload["body"]["LimitPriceProfitOrder"] = boco.LimitPriceProfitOrder
        self.payload["body"]["TriggerPriceForSL"] = boco.TriggerPriceForSL
        self.payload["body"]["TrailingSL"] = boco.TrailingSL
        self.payload["body"]["StopLoss"] = boco.StopLoss
        self.payload["body"]["ScripCode"] = boco.scrip_code
        self.payload["body"]["OrderFor"] = boco.order_for
        self.payload["body"]["UniqueOrderIDNormal"] = boco.UniqueOrderIDNormal
        self.payload["body"]["UniqueOrderIDSL"] = boco.UniqueOrderIDSL
        self.payload["body"]["UniqueOrderIDLimit"] = boco.UniqueOrderIDLimit
        self.payload["body"]["LocalOrderIDNormal"] = boco.LocalOrderIDNormal
        self.payload["body"]["LocalOrderIDSL"] = boco.LocalOrderIDSL
        self.payload["body"]["LocalOrderIDLimit"] = boco.LocalOrderIDLimit
        self.payload["body"]["PublicIP"] = boco.public_ip
        self.payload["body"]["AppSource"] = self.APP_SOURCE
        self.payload["body"]["TradedQty"] = boco.traded_qty

    def place_order(self, order: Order):
        """
        Places a fresh order
        """
        self.set_payload(order)
        self.payload["body"]["StopLossPrice"] = order.stoploss_price
        return self.order_request("OP")

    def modify_order(self, order: Order):
        """
        Modifies an existing order
        """
   
        self.set_payload(order)
        self.payload["body"]["StopLossPrice"] = order.stoploss_price
        self.payload["body"]["OrderFor"] = "M"
        
        return self.order_request("OP")

    def cancel_order(self,order_type:str, scrip_code:int, quantity:int,exchange:str,exchange_segment:str,exch_order_id:str):
        """
        Cancels an existing order
        """
        order = Order(order_type=order_type, scrip_code=scrip_code,
                      quantity=quantity,exchange=exchange,exchange_segment=exchange_segment, exch_order_id=exch_order_id, price=0.0,atmarket=False,is_intraday=False,order_for='C')
        self.set_payload(order)
        self.payload["body"]["StopLossPrice"] = order.stoploss_price
        return self.order_request("OP")
    
    def bo_order(self,boco:bo_co_order):
        self.set_payload_bo(boco)
        return self.order_request("BO")

    def mod_bo_order(self,order: Order):
        self.set_payload(order)
        self.payload["body"]["TriggerPriceForSL"] = order.stoploss_price
        return self.order_request("BM")
    
    def Request_Feed(self,Method:str,Operation:str,req_list:list):
        Method_dict={"mf":"MarketFeedV3","md":"MarketDepthService","oi":"GetScripInfoForFuture"}
        Operation_dict={"s":"Subscribe","u":"Unsubscribe"}
        
        self.ws_payload['Method']=Method_dict[Method]
        self.ws_payload['Operation']=Operation_dict[Operation]
        self.ws_payload['ClientCode']=self.client_code
        self.ws_payload['MarketFeedData']=req_list
        return self.ws_payload
    def Streming_data(self,wsPayload : dict):
        self.web_url=f'wss://openfeed.5paisa.com/Feeds/api/chat?Value1={self.Jwt_token}|{self.client_code}'
        auth=self.Login_check()
        
        def on_message(ws, message):
            print(message)
        
        def on_error(ws, error):
            print(error)
            
        def on_close(ws):
            print("Streaming Stopped")
        
        def on_open(ws):
            print("Streaming Started")
            ws.send(json.dumps(wsPayload))
        
            
        ws = websocket.WebSocketApp(self.web_url,
                              on_open=on_open,
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close,
                              cookie=auth)
        
        ws.run_forever()
        
    def Login_check(self):
        self.login_check_payload["head"]["key"]=self.USER_KEY
        self.login_check_payload["head"]["appName"]=self.APP_NAME
        self.login_check_payload["head"]["LoginId"]=self.client_code
        self.login_check_payload["body"]["RegistrationID"]=self.Jwt_token
        url=self.LOGIN_CHECK_ROUTE
        resl=requests.post(url, json=self.login_check_payload,headers=HEADERS)
        self.Aspx_auth = resl.cookies.get('.ASPXAUTH',domain='openfeed.5paisa.com')
        
        return f'.ASPXAUTH={self.Aspx_auth}'

    def jwt_validate(self):
        self.jwt_payload['ClientCode']=self.client_code
        self.jwt_payload['JwtCode']=self.Jwt_token
        url=self.JWT_VALIDATION_ROUTE
        response = self.session.post(url, json=self.jwt_payload, headers=HEADERS).json()
        
        return response['body']['Message']

    def historical_data(self,Exch:str,ExchangeSegment:str,ScripCode: int,time: str,From:str,To: str):
        validation=self.jwt_validate()
        
        
        if validation=='Authorization Successful':
            self.jwt_headers['x-clientcode']=self.client_code
            self.jwt_headers['x-auth-token']=self.Jwt_token
            url=f'{self.HISTORICAL_DATA_ROUTE}{Exch}/{ExchangeSegment}/{ScripCode}/{time}?from={From}&end={To}'
            timeList=['1m','5m','10m','15m','30m','60m','1d']
            if time not in timeList:
                return 'Invalid Time Frame. it should be within [1m,5m,10m,15m,30m,60m,1d].'
            else:
                
                
                response = self.session.get(url, headers=self.jwt_headers).json()
                candleList=response['data']['candles']
                
                df=pd.DataFrame(candleList)
        
                df.columns=['Datetime','Open','High','Low','Close','Volume']
        
                return df
        
        else:
            return 'Invalid JWT.'

    def get_buy(self):
        res=self._user_info_request("IB")
        if len(res) > 0:
            message = res[0]["payload"]
            res1 = json.loads(message)
            with pd.option_context('display.max_columns',None,'display.max_rows',None):
                df=pd.DataFrame(res1)
            return df
        else:
            message ="You don't have an active Ultra-Trader-Pack. Please subscribe to it to avail the services."
            return message

    def get_trade(self):
        res=self._user_info_request("IT")
        if len(res) > 0:
            message = res[1]["payload"]
            res1 = json.loads(message)
            with pd.option_context('display.max_columns',None,'display.max_rows',None):
                df=pd.DataFrame(res1)
            return df
        else:
            message ="You don't have an active Ultra-Trader-Pack. Please subscribe to it to avail the services."
            return message


    def get_tradebook(self):
        return self.order_request("TB")
        

        
        
    
        



      
     
