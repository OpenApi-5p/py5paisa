
BaseUrl='https://Openapi.5paisa.com/VendorsAPI/Service1.svc/'



LOGIN_ROUTE = f'{BaseUrl}V4/LoginRequestMobileNewbyEmail'

MARGIN_ROUTE = f'{BaseUrl}V3/Margin'
ORDER_BOOK_ROUTE = f'{BaseUrl}V2/OrderBook'
HOLDINGS_ROUTE = f'{BaseUrl}V2/Holding'
POSITIONS_ROUTE = f'{BaseUrl}V1/NetPositionNetWise'

ORDER_PLACEMENT_ROUTE = f'{BaseUrl}/V1/PlaceOrderRequest'
ORDER_MODIFY_ROUTE= f'{BaseUrl}/V1/ModifyOrderRequest'
ORDER_CANCEL_ROUTE= f'{BaseUrl}/V1/CancelOrderRequest'
ORDER_STATUS_ROUTE = f'{BaseUrl}/V1/OrderStatus'
TRADE_INFO_ROUTE = f'{BaseUrl}TradeInformation'

BRACKET_MOD_ROUTE= f'{BaseUrl}ModifySMOOrder'
BRACKET_ORDER_ROUTE= f'{BaseUrl}SMOOrderRequest'

MARKET_FEED_ROUTE= f'{BaseUrl}MarketFeed'
LOGIN_CHECK_ROUTE="https://openfeed.5paisa.com/Feeds/api/UserActivity/LoginCheck"

MARKET_DEPTH_ROUTE= f'{BaseUrl}/MarketDepth'
MARKET_DEPTH_BY_SYMBOL_ROUTE= f'{BaseUrl}/V1/MarketDepth'
JWT_VALIDATION_ROUTE="https://Openapi.indiainfoline.com/VendorsAPI/Service1.svc/JWTOpenApiValidation"
HISTORICAL_DATA_ROUTE="https://openapi.5paisa.com/historical/"

IDEAS_ROUTE= f'{BaseUrl}TraderIDEAs'

TRADEBOOK_ROUTE= f'{BaseUrl}V1/TradeBook'

ACCESS_TOKEN_ROUTE=  f'{BaseUrl}GetAccessToken'
MARKET_STATUS_ROUTE=  f'{BaseUrl}MarketStatus'
TRADE_HISTORY_ROUTE=  f'{BaseUrl}TradeHistory'

GET_BASKET_ROUTE=  f'{BaseUrl}GetBaskets'
CREATE_BASKET_ROUTE= f'{BaseUrl}CreateBasket'
RENAME_BASKET_ROUTE= f'{BaseUrl}EditBasketName'
DELETE_BASKET_ROUTE= f'{BaseUrl}DeleteBasket'
CLONE_BASKET_ROUTE= f'{BaseUrl}CloneBasket'
EXECUTE_BASKET_ROUTE= f'{BaseUrl}ExecuteBasket'
GET_ORDER_IN_BASKET_ROUTE= f'{BaseUrl}GetOrderInBasket'
ADD_BASKET_ORDER_ROUTE= f'{BaseUrl}AddOrderToBasket'
OPTION_CHAIN_ROUTE=f'{BaseUrl}V2/GetExpiryForSymbolOptions'
GET_OPTION_CHAIN_ROUTE=f'{BaseUrl}GetOptionsForSymbol'
CANCEL_BULK_ORDER_ROUTE=f'{BaseUrl}CancelOrderBulk'
SQUAREOFF_ROUTE=f'{BaseUrl}SquareOffAll'
POSITION_CONVERSION_ROUTE=f'{BaseUrl}PositionConversion'
MARKET_DEPTH_ROUTE="https://openapi.5paisa.com/marketfeed-token/token"
