from py5paisa.strategy import *

cred={
    "APP_NAME":"5P50052770",
    "APP_SOURCE":"10345",
    "USER_ID":"fdiUhA4mBNO",
    "PASSWORD":"jalna7w0RuA",
    "USER_KEY":"giQIoatyGcXADwxV05uWHiOW2QOWNLcs",
    "ENCRYPTION_KEY":"dlXKxViN7yLMIaDc3RpCJzZeqwSvYbu7"
    }

strategy=strategies(user="bhaveshshirode1@gmail.com", passw="Quant@123", dob="19931214",cred=cred)
#strategy=strategies()

strategy.short_strangle("banknifty",['38400','40200'],'50','20220922','D',tag='strangle')
#strategy.short_straddle("banknifty",'41400','50','20220922','D',tag='straddle')
#strategy.long_straddle("banknifty",'41400','50','20220922','I',tag='long_straddle')
#strategy.iron_condor("NIFTY",["17000","17200"],["17100","17150"],"50","20220922","I",tag='iron_condor')
