import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .auth import EncryptionClient
from .const import GENERIC_PAYLOAD, LOGIN_PAYLOAD, HEADERS, NEXT_DAY_TIMESTAMP, TODAY_TIMESTAMP,LOGIN_CHECK_PAYLOAD,WS_PAYLOAD,JWT_PAYLOAD,JWT_HEADERS
from .order import Order, bo_co_order
from .logging import log_response
import json
import websocket
import pandas as pd
import websocket 
from .urlconst  import *


class FivePaisaClient:
   
    def __init__(self, email=None, passwd=None, dob=None,cred=None):
        """
        Main constructor for client.
        Expects user's email, password and date of birth in YYYYMMDD format.
        """
        try:
            self.email = email
            self.passwd = passwd
            self.dob = dob
            self.client_code = None
            self.Jwt_token = None
            self.Aspx_auth = None
            self.web_url= None
            self.Res_Data= None
            self.ws= None
            self.access_token= ""
            self.session = requests.Session()
            self.APP_SOURCE=cred["APP_SOURCE"]
            self.APP_NAME=cred["APP_NAME"]
            self.USER_ID=cred["USER_ID"]
            self.PASSWORD=cred["PASSWORD"]
            self.USER_KEY=cred["USER_KEY"]
            self.ENCRYPTION_KEY=cred["ENCRYPTION_KEY"]
            self.create_payload()
            self.set_url()
        except Exception as e:
            log_response(e)
    

    def login(self):
        try:
            encryption_client = EncryptionClient(self.ENCRYPTION_KEY)
            secret_email = encryption_client.encrypt(self.email)
            secret_passwd = encryption_client.encrypt(self.passwd)
            secret_dob = encryption_client.encrypt(self.dob)
            self.login_payload["body"]["Email_id"] = secret_email
            self.login_payload["body"]["Password"] = secret_passwd
            self.login_payload["body"]["My2PIN"] = secret_dob
            self.login_payload["head"]["requestCode"] = "5PLoginV4"
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
        except Exception as e:
            log_response(e)

    def holdings(self):
        try:
            return self._user_info_request("HOLDINGS")
        except Exception as e:
            log_response(e)

    def margin(self):
        try:
            return self._user_info_request("MARGIN")
        except Exception as e:
            log_response(e)

    def order_book(self):
        try:
            return self._user_info_request("ORDER_BOOK")
        except Exception as e:
            log_response(e)

    def positions(self):
        try:
            return self._user_info_request("POSITIONS")
        except Exception as e:
            log_response(e)

    def _login_request(self, route):
        try:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            res = self.session.post(route, json=self.login_payload, headers=HEADERS)
            resp=res.json()
            self.Jwt_token=resp["body"]["JWTToken"]
            return res.json()
        except Exception as e:
            log_response(e)

    def _set_client_code(self, client_code):
        try:
            self.client_code = client_code
        except Exception as e:
            log_response(e)

    def _user_info_request(self, data_type):
        try:
            payload = GENERIC_PAYLOAD
            payload["body"]["ClientCode"] = self.client_code
            payload["head"]["key"] = self.USER_KEY
            return_type = ""
            if data_type == "MARGIN":
                url = self.MARGIN_ROUTE
                return_type = "EquityMargin"
            elif data_type == "ORDER_BOOK":
                url = self.ORDER_BOOK_ROUTE
                return_type = "OrderBookDetail"
            elif data_type == "HOLDINGS":
                url = self.HOLDINGS_ROUTE
                return_type = "Data"
            elif data_type == "POSITIONS":
                url = self.POSITIONS_ROUTE
                return_type = "NetPositionDetail"
            elif data_type == "IB":
                url = self.IDEAS_ROUTE
                return_type = "Data"
            elif data_type == "IT":
                url = self.IDEAS_ROUTE
                return_type = "Data"
            else:
                raise Exception("Invalid data type requested")

            response = self.session.post(url, json=payload, headers=HEADERS).json()
            
            data = response["body"][return_type]
            return data
        except Exception as e:
            log_response(e)

    def order_request(self, req_type) -> None:
        try:
            self.payload["body"]["ClientCode"] = self.client_code
            self.payload["head"]["key"] = self.USER_KEY
            if req_type == "OP":
                url = self.ORDER_PLACEMENT_ROUTE
                HEADERS["Authorization"] = f'Bearer {self.Jwt_token}'
            elif req_type == "OC":
                url = self.ORDER_CANCEL_ROUTE
                HEADERS["Authorization"] = f'Bearer {self.Jwt_token}'
            elif req_type == "OM":
                url = self.ORDER_MODIFY_ROUTE
                HEADERS["Authorization"] = f'Bearer {self.Jwt_token}'
            elif req_type == "OS":
                url = self.ORDER_STATUS_ROUTE
            elif req_type == "TI":
                url = self.TRADE_INFO_ROUTE
            elif req_type == "MF":
                url = self.MARKET_FEED_ROUTE
                self.payload["body"]["COUNT"]=self.client_code
            elif req_type == "BM":
                url = self.BRACKET_MOD_ROUTE
                self.payload["body"]["legtype"]=0
                self.payload["body"]["TMOPartnerOrderID"]=0
            elif req_type == "BO":
                url = self.BRACKET_ORDER_ROUTE
                self.payload["body"]["OrderRequesterCode"]=self.client_code
            elif req_type == "MD":
                url = self.MARKET_DEPTH_ROUTE
            elif req_type == "TB":
                url = self.TRADEBOOK_ROUTE
            elif req_type == "MS":
                url = self.MARKET_STATUS_ROUTE
                self.payload["body"]["ClientCode"] = ""
                HEADERS["Authorization"] = f'Bearer {self.access_token}'
            elif req_type == "TH":
                url = self.TRADE_HISTORY_ROUTE
                HEADERS["Authorization"] = f'Bearer {self.access_token}'
                
            else:
                raise Exception("Invalid request type!")
            
            res = self.session.post(url, json=self.payload,
                                    headers=HEADERS).json()
            if req_type == "MS":
                log_response(res["head"]["statusDescription"])
            else:
                log_response(res["body"]["Message"])
            return res["body"]
        except Exception as e:
            log_response(e)

    def fetch_order_status(self, req_list:list) :
        try:
            self.payload["body"]["OrdStatusReqList"] = req_list
            return self.order_request("OS")
        except Exception as e:
            log_response(e)

    def fetch_trade_info(self, req_list:list) :
        try:
            self.payload["body"]["TradeInformationList"] = req_list
            return self.order_request("TI")
        except Exception as e:
            log_response(e)

    def fetch_market_depth(self, req_list:list):
        try:
            self.payload["body"]["Count"]="1"
            self.payload["body"]["Data"]=req_list
        
            return self.order_request("MD")
        except Exception as e:
            log_response(e)
    
    def fetch_market_feed(self, req_list:list) :
        """
            market feed api
        """
        try:
            self.payload["body"]["MarketFeedData"] = req_list
            self.payload["body"]["ClientLoginType"] = 0
            self.payload["body"]["LastRequestTime"] = f"/Date({TODAY_TIMESTAMP})/"
            self.payload["body"]["RefreshRate"] = "H"
            return self.order_request("MF")
        except Exception as e:
            log_response(e)

    def set_payload(self, order: Order) -> None:
        try:
            self.payload["body"]["Exchange"] = order.exchange
            self.payload["body"]["ExchangeType"] = order.exchange_segment
            self.payload["body"]["Price"] = order.price
            self.payload["body"]["OrderID"] = order.order_id
            if order.scrip_code != 0:
                self.payload["body"]["ScripCode"] = order.scrip_code
            else:
                self.payload["body"]["ScripData"] = order.scripData
            if order.IsGTCOrder:
                self.payload["body"]["IsGTCOrder"] = order.IsGTCOrder
            if order.IsEOSOrder:
                self.payload["body"]["IsEOSOrder"] = order.IsEOSOrder
            self.payload["body"]["Qty"] = order.quantity
            self.payload["body"]["IsAHOrder"] = order.ahplaced
            self.payload["body"]["DisQty"] = order.disqty
            self.payload["body"]["IsStopLossOrder"] = str(
                order.is_stoploss_order).lower()
            self.payload["body"]["IsIOCOrder"] = str(order.ioc_order).lower()
            self.payload["body"]["IsIntraday"] = str(order.is_intraday).lower()
            self.payload["body"]["StopLossPrice"] = order.stoploss_price
            # Passing the next day's UNIX timestamp
            self.payload["body"]["ValidTillDate"] = f"/Date({NEXT_DAY_TIMESTAMP})/"
            self.payload["body"]["AppSource"] = self.APP_SOURCE
        except Exception as e:
            log_response(e)
        
        
    def set_payload_bo(self,boco:bo_co_order)-> None:
        """
            this is for bo-co order placement
        """
        try:
            self.payload["body"]["RequestType"] = boco.RequestType
            self.payload["body"]["BuySell"] = boco.BuySell
            self.payload["body"]["Qty"] = boco.Qty
            self.payload["body"]["Exch"] = boco.Exch
            self.payload["body"]["ExchType"] = boco.ExchType
            self.payload["body"]["DisQty"] = boco.DisQty
            self.payload["body"]["AtMarket"] = boco.AtMarket
            self.payload["body"]["ExchOrderId"] = boco.ExchOrderId
            self.payload["body"]["LimitPriceForSL"] = boco.LimitPriceForSL
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
        except Exception as e:
            log_response(e)

    def place_order(self, order: Order):
        """
        Places a fresh order
        """
        try:
            self.set_payload(order)
            self.payload["body"]["OrderType"] = order.order_type
            self.payload["body"]["RemoteOrderID"] = order.remote_order_id
            
            return self.order_request("OP")
        except Exception as e:
            log_response(e)

    def modify_order(self, order: Order):
        """
        Modifies an existing order
        """
        try:
            self.set_payload(order)
            self.payload["body"]["ExchOrderID"] = order.exch_order_id
        
            return self.order_request("OM")
        except Exception as e:
            log_response(e)

    def cancel_order(self,exchange:str,exchange_segment:str,exch_order_id:str):
        """
        Cancels an existing order
        """
        try:
            self.payload["body"]["Exchange"]=exchange
            self.payload["body"]["ExchangeType"]=exchange_segment
            self.payload["body"]["ExchOrderID"]=exch_order_id
            self.payload["body"]["AppSource"]=self.APP_SOURCE
            return self.order_request("OC")
        except Exception as e:
            log_response(e)

    def bo_order(self,boco:bo_co_order):
        try:
            self.set_payload_bo(boco)
            return self.order_request("BO")
        except Exception as e:
            log_response(e)

    def mod_bo_order(self,order: Order):
        try:
            self.set_payload(order)
            self.payload["body"]["TriggerPriceForSL"] = order.stoploss_price
            return self.order_request("BM")
        except Exception as e:
            log_response(e)
    
    def Request_Feed(self,Method:str,Operation:str,req_list:list):
        try:
            Method_dict={"mf":"MarketFeedV3","md":"MarketDepthService","oi":"GetScripInfoForFuture","i":"Indices"}
            Operation_dict={"s":"Subscribe","u":"Unsubscribe"}
        
            self.ws_payload['Method']=Method_dict[Method]
            self.ws_payload['Operation']=Operation_dict[Operation]
            self.ws_payload['ClientCode']=self.client_code
            self.ws_payload['MarketFeedData']=req_list
            return self.ws_payload
        except Exception as e:
            log_response(e)
    
    def connect(self,wspayload:dict):
        try:
            self.web_url=f'wss://openfeed.5paisa.com/Feeds/api/chat?Value1={self.Jwt_token}|{self.client_code}'
            
            def on_open(ws):
                log_response("Streaming Started")
                try: 
                    ws.send(json.dumps(wspayload))
                except Exception as e:
                    log_response(e)
            self.ws = websocket.WebSocketApp(self.web_url)

            self.ws.on_open=on_open
        except Exception as e:
            log_response(e)
       
    
        
    def send_data(self,open_:any):
        try:
            self.ws.on_open=open_
        except Exception as e:
            log_response(e)

    def receive_data(self,msg:any):
        try:
            self.ws.on_message=msg
            self.ws.run_forever()
        except Exception as e:
            log_response(e)

    def close_data(self):
        try:
            self.ws.close()
        except Exception as e:
            log_response(e)

    def error_data(self,err:any):
        try:
            self.ws.on_error=err
        except Exception as e:
            log_response(e)
        
    def Login_check(self):
        try:
            self.login_check_payload["head"]["key"]=self.USER_KEY
            self.login_check_payload["head"]["appName"]=self.APP_NAME
            self.login_check_payload["head"]["LoginId"]=self.client_code
            self.login_check_payload["body"]["RegistrationID"]=self.Jwt_token
            url=self.LOGIN_CHECK_ROUTE
            resl=requests.post(url, json=self.login_check_payload,headers=HEADERS)
            self.Aspx_auth = resl.cookies.get('.ASPXAUTH',domain='openfeed.5paisa.com')
            
            return f'.ASPXAUTH={self.Aspx_auth}'
        except Exception as e:
            log_response(e)

    def jwt_validate(self):
        try:
            self.jwt_payload['ClientCode']=self.client_code
            self.jwt_payload['JwtCode']=self.Jwt_token
            url=self.JWT_VALIDATION_ROUTE
            response = self.session.post(url, json=self.jwt_payload, headers=HEADERS).json()
            
            return response['body']['Message']
        except Exception as e:
            log_response(e)

    def historical_data(self,Exch:str,ExchangeSegment:str,ScripCode: int,time: str,From:str,To: str):
        try:
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
        except Exception as e:
            log_response(e)

    def get_buy(self):
        try:
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
        except Exception as e:
            log_response(e)

    def get_trade(self):
        try:
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
        except Exception as e:
            log_response(e)


    def get_tradebook(self):
        try:
            return self.order_request("TB")
        except Exception as e:
            log_response(e)

    def set_url(self):
        try:
            self.LOGIN_ROUTE=LOGIN_ROUTE
            self.MARGIN_ROUTE=MARGIN_ROUTE
            self.ORDER_BOOK_ROUTE=ORDER_BOOK_ROUTE
            self.HOLDINGS_ROUTE=HOLDINGS_ROUTE
            self.POSITIONS_ROUTE=POSITIONS_ROUTE
            self.ORDER_PLACEMENT_ROUTE=ORDER_PLACEMENT_ROUTE
            self.ORDER_MODIFY_ROUTE=ORDER_MODIFY_ROUTE
            self.ORDER_CANCEL_ROUTE=ORDER_CANCEL_ROUTE
            self.ORDER_STATUS_ROUTE=ORDER_STATUS_ROUTE
            self.TRADE_INFO_ROUTE=TRADE_INFO_ROUTE
            self.BRACKET_MOD_ROUTE=BRACKET_MOD_ROUTE
            self.BRACKET_ORDER_ROUTE=BRACKET_ORDER_ROUTE
            self.MARKET_FEED_ROUTE=MARKET_FEED_ROUTE
            self.LOGIN_CHECK_ROUTE=LOGIN_CHECK_ROUTE
            self.MARKET_DEPTH_ROUTE=MARKET_DEPTH_ROUTE
            self.JWT_VALIDATION_ROUTE=JWT_VALIDATION_ROUTE
            self.HISTORICAL_DATA_ROUTE=HISTORICAL_DATA_ROUTE
            self.IDEAS_ROUTE=IDEAS_ROUTE
            self.TRADEBOOK_ROUTE=TRADEBOOK_ROUTE
            self.ACCESS_TOKEN_ROUTE=ACCESS_TOKEN_ROUTE
            self.MARKET_STATUS_ROUTE=MARKET_STATUS_ROUTE
            self.TRADE_HISTORY_ROUTE=TRADE_HISTORY_ROUTE
        except Exception as e:
            log_response(e)
    

    def create_payload(self):
        try:
            self.payload = GENERIC_PAYLOAD
            self.login_payload = LOGIN_PAYLOAD
            self.login_check_payload= LOGIN_CHECK_PAYLOAD
            self.ws_payload=WS_PAYLOAD
            self.jwt_headers=JWT_HEADERS
            self.jwt_payload=JWT_PAYLOAD
        except Exception as e:
            log_response(e)
        
    def get_access_token(self,request_token):
        try:
            self.payload["head"]["Key"] = self.USER_KEY
            self.payload["body"]["RequestToken"] = request_token
            self.payload["body"]["EncryKey"] = self.ENCRYPTION_KEY
            self.payload["body"]["UserId"] = self.USER_ID
            url=ACCESS_TOKEN_ROUTE

            res = self.session.post(url, json=self.payload).json()
            message = res["body"]["Message"]
         
            if message == "Success":
                self.access_token=res["body"]["AccessToken"]
                self._set_client_code(res["body"]["ClientCode"])
                return self.access_token
            else:
                log_response(message)
        except Exception as e:
            log_response(e)

    def get_market_status(self):
        try:
            market_status_response=self.order_request("MS")
            return market_status_response["Data"]
        except Exception as e:
            log_response(e)

    def get_trade_history(self,exchange_id):
        try:
            self.payload["body"]["ExchOrderID"] = exchange_id
            if self.client_code != None:
                return self.order_request("TH")
        except Exception as e:
            log_response(e)
        
 
