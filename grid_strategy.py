import yfinance as yf
import pandas as pd
import numpy as np
import pandas_ta as ta
import backtesting

from backtesting import Strategy
from backtesting import Backtest


data = yf.download("EURUSD=X", start="2023-01-01", end="2023-01-13", interval='5m')
data.iloc[:,:]

grid_distance = 0.005
TPSL_Ratio = 1
midprice = 1.065

print(data)

def generate_grid(midprice, grid_distance, grid_range):
    return (np.arange(midprice-grid_range, midprice+grid_range, grid_distance))

grid = generate_grid(midprice, grid_distance, 0.1)
print(grid)

signal = [0]*len(data)
i=0
for index, row in data.iterrows():
    for p in grid:
        if min(row.Low, row.High)<p and max(row.Low, row.High)>p:
            signal[i]=1
    i+=1


data["signal"]=signal
data[data["signal"]==1]

dfpl = data[:].copy()
def SIGNAL():
    return dfpl.signal
dfpl['ATR'] = ta.atr(high = dfpl.High, low = dfpl.Low, close = dfpl.Close, length = 16)
dfpl.dropna(inplace=True)


class MyStrat(Strategy):
    mysize = 0.5

    def init(self):
        super().init()
        self.signal1 = self.I(SIGNAL)

    def next(self):
        super().next()
        slatr = self.data.ATR[-1]  # grid_distance
        TPSLRatio = 1.2 * TPSL_Ratio

        if self.signal1 == 1 and len(self.trades) <= 2:
            sl1 = self.data.Close[-1] - slatr
            tp1 = self.data.Close[-1] + slatr * TPSLRatio
            self.buy(sl=sl1, tp=tp1, size=self.mysize)

            sl1 = self.data.Close[-1] + slatr
            tp1 = self.data.Close[-1] - slatr * TPSLRatio
            self.sell(sl=sl1, tp=tp1, size=self.mysize)


stat = Backtest(dfpl, MyStrat, cash=100, margin=1 / 1, commission=.000).run()

stat
print(stat)
