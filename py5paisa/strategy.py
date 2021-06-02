# These are standard 

from py5paisa import FivePaisaClient
from py5paisa.order import Order,bo_co_order
from .conf import user,passw,dob

Client=FivePaisaClient(email=user, passwd=passw, dob=dob)
Client.login()

#market feed api
# req_list_=[{"Exch":"N","ExchType":"D","Symbol":"NIFTY 20 MAY 2021 CE 14500.00","Expiry":"20210520","StrikePrice":"14500","OptionType":"CE"},{"Exch":"N","ExchType":"D","Symbol":"NIFTY 27 MAY 2021","Expiry":"20210527","StrikePrice":"0","OptionType":"XX"},{"Exch":"B","ExchType":"C","Symbol":"LT"},{"Exch":"M","ExchType":"D","Symbol":"GOLD"}]           
# print(Client.fetch_market_feed(req_list_))
# short_straddle("NIFTY",15000,75)

class strategies:
    # def __init__(self,symbol,strike,qty,expiry):
    #     self.symbol=symbol
    #     self.strike=strike
    #     self.qty=qty
    #     self.expiry=expiry

    def get_scripcode(self,symbol,strike,expiry,opt):
        month={
            "01":'JAN',
            "02":'FEB',
            "03":'MAR',
            "04":'APR',
            "05":'MAY',
            "06":'JUN',
            "07":'JUL',
            "08":'AUG',
            "09":'SEP',
            "10":'OCT',
            "11":'NOV',
            "12":'DEC'      
        }
        date=expiry[6:]
        mon=month[expiry[4:6]]
        year=expiry[:4]
        symbol=symbol.upper()
        strike_f="{:.2f}".format(float(strike))
        sym=f'{symbol} {date} {mon} {year} {opt} {strike_f}'
        print(sym)
        req=[{"Exch":"N","ExchType":"D","Symbol":sym,"Expiry":expiry,"StrikePrice":strike,"OptionType":opt}]
        res=Client.fetch_market_feed(req)
        token=res['Data'][0]['Token']
        return token

    def intraday(self,intra):
        if intra=='I':
            return True
        else:
            return False

    def short_straddle(self,symbol,strike,qty,expiry,intra):
        self.symbol=symbol
        self.strike=strike
        self.qty=qty
        self.expiry=expiry
        self.intra=intra
        scrip=[]
        options =['CE','PE']
        #Get Scrip code
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.strike,self.expiry,opt)
            scrip.append(sc)
         
        for s in scrip:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True,)
            order_status=Client.place_order(test_order)
            print(order_status)
            if order_status['Message']=='Success':
                continue
            else:
                break
    #short_strangle(self,"NIFTY",[15000,15200],qty,expiry)
    def short_strangle(self,symbol,strike,qty,expiry,intra):
        self.symbol=symbol
        self.strike=strike
        self.qty=qty
        self.expiry=expiry
        self.intra=intra
        scrip=[]
        i=0
        options =['PE','CE']
        #Get Scrip code
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.strike[i],self.expiry,opt)
            i=i+1
            scrip.append(sc)
         
        for s in scrip:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True)
            order_status=Client.place_order(test_order)
            if order_status['Message']=='Success':
                continue
            else:
                break

    def long_straddle(self,symbol,strike,qty,expiry,intra):
        self.symbol=symbol
        self.strike=strike
        self.qty=qty
        self.expiry=expiry
        self.intra=intra
        scrip=[]
        options =['CE','PE']
        #Get Scrip code
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.strike,self.expiry,opt)
            scrip.append(sc)
         
        for s in scrip:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True)
            order_status=Client.place_order(test_order)
            if order_status['Message']=='Success':
                continue
            else:
                break
    #long_strangle(self,"NIFTY",["15000","15200"],qty,expiry)
    def long_strangle(self,symbol,strike,qty,expiry,intra):
        self.symbol=symbol
        self.strike=strike
        self.qty=qty
        self.expiry=expiry
        self.intra=intra
        scrip=[]
        i=0
        options =['PE','CE']
        #Get Scrip code
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.strike[i],self.expiry,opt)
            i=i+1
            scrip.append(sc)
         
        for s in scrip:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True)
            order_status=Client.place_order(test_order)
            if order_status['Message']=='Success':
                continue
            else:
                break
    #iron_fly(self,"NIFTY",["15000","15200"],qty,expiry,intra)
    def iron_fly(self,symbol,buy_strike,sell_strike,qty,expiry,intra):
        self.symbol=symbol
        self.buy_strike=buy_strike
        self.sell_strike=sell_strike
        self.qty=qty
        self.expiry=expiry
        self.intra=intra
        buy_scrip=[]
        sell_scrip=[]
        i=0
        options =['PE','CE']
        #Get Scrip code
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.buy_strike[i],self.expiry,opt)
            i=i+1
            buy_scrip.append(sc)
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.sell_strike,self.expiry,opt)
            sell_scrip.append(sc)
        print(buy_scrip,sell_scrip)
        for s in buy_scrip:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True)
            order_status=Client.place_order(test_order)
            if order_status['Message']=='Success':
                continue
            else:
                break
        for s in sell_scrip:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True)
            order_status=Client.place_order(test_order)
            if order_status['Message']=='Success':
                continue
            else:
                break
    
    #iron_condor(<symbol>,<List of buy strike prices>,<List of sell strike price>,<qty>,<expiry>,<Order Type>)
    #iron_condor("NIFTY",["15000","15200"],["15000","15200"],"75","20210603",I/D)
    def iron_condor(self,symbol,buy_strike,sell_strike,qty,expiry,intra):
        self.symbol=symbol
        self.buy_strike=buy_strike
        self.sell_strike=sell_strike
        self.qty=qty
        self.expiry=expiry
        self.intra=intra
        buy_scrip=[]
        sell_scrip=[]
        i=0
        j=0
        options =['PE','CE']
        #Get Scrip code
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.buy_strike[i],self.expiry,opt)
            i=i+1
            buy_scrip.append(sc)
        for opt in options:
            sc=self.get_scripcode(self.symbol,self.sell_strike[j],self.expiry,opt)
            j=j+1
            sell_scrip.append(sc)
        print(buy_scrip,sell_scrip)
        for s in buy_scrip:
            test_order = Order(order_type='B',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True,)
            order_status=Client.place_order(test_order)
            if order_status['Message']=='Success':
                continue
            else:
                break
        for s in sell_scrip:
            test_order = Order(order_type='S',exchange='N',exchange_segment='D', scrip_code=s, quantity=qty, price=0,is_intraday=self.intraday(self.intra),atmarket=True)
            order_status=Client.place_order(test_order)
            if order_status['Message']=='Success':
                continue
            else:
                break
  


#ob.iron_condor("nifty",["15000","15600"],["15300","15400"],"75","20210603")
#ob.iron_fly("nifty",["15200","15600"],"15400","75","20210603") 