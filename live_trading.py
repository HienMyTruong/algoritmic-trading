from apscheduler.schedulers.blocking import BlockingScheduler

from oandapyV20 import API
import pandas as pd
import oandapyV20.endpoints.orders as orders
from oandapyV20.contrib.requests import MarketOrderRequest
from oanda_candles import Pair, Gran, CandleClient
from oandapyV20.contrib.requests import TakeProfitDetails, StopLossDetails

from test_signal import signal_generator

access_token = "XXXXXX"
accountID = "OANDA account"
def get_candles(n):
    #access_token='XXXXXXX'#you need token here generated from OANDA account
    client = CandleClient(access_token, real=False)
    collector = client.get_collector(Pair.EUR_USD, Gran.M15)
    candles = collector.grab(n)
    return candles

candles = get_candles(3)
for candle in candles:
    print(float(str(candle.bid.o))>1)


def trading_job():
    candles = get_candles(3)
    dfstream = pd.DataFrame(columns=['Open', 'Close', 'High', 'Low'])

    i = 0
    for candle in candles:
        dfstream.loc[i, ['Open']] = float(str(candle.bid.o))
        dfstream.loc[i, ['Close']] = float(str(candle.bid.c))
        dfstream.loc[i, ['High']] = float(str(candle.bid.h))
        dfstream.loc[i, ['Low']] = float(str(candle.bid.l))
        i = i + 1

    dfstream['Open'] = dfstream['Open'].astype(float)
    dfstream['Close'] = dfstream['Close'].astype(float)
    dfstream['High'] = dfstream['High'].astype(float)
    dfstream['Low'] = dfstream['Low'].astype(float)

    signal = signal_generator(dfstream.iloc[:-1, :])  #

    # EXECUTING ORDERS
    # accountID = "XXXXXXX" #your account ID here
    client = API(access_token)

    SLTPRatio = 2.
    previous_candleR = abs(dfstream['High'].iloc[-2] - dfstream['Low'].iloc[-2])

    SLBuy = float(str(candle.bid.o)) - previous_candleR
    SLSell = float(str(candle.bid.o)) + previous_candleR

    TPBuy = float(str(candle.bid.o)) + previous_candleR * SLTPRatio
    TPSell = float(str(candle.bid.o)) - previous_candleR * SLTPRatio

    print(dfstream.iloc[:-1, :])
    print(TPBuy, "  ", SLBuy, "  ", TPSell, "  ", SLSell)
    signal = 2
    # Sell
    if signal == 1:
        mo = MarketOrderRequest(instrument="EUR_USD", units=-1000,
                                takeProfitOnFill=TakeProfitDetails(price=TPSell).data,
                                stopLossOnFill=StopLossDetails(price=SLSell).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)
    # Buy
    elif signal == 2:
        mo = MarketOrderRequest(instrument="EUR_USD", units=1000, takeProfitOnFill=TakeProfitDetails(price=TPBuy).data,
                                stopLossOnFill=StopLossDetails(price=SLBuy).data)
        r = orders.OrderCreate(accountID, data=mo.data)
        rv = client.request(r)
        print(rv)