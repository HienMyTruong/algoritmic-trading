import yfinance as yf
import pandas as pd

data = yf.download("EURUSD=X", start="2023-01-01", end="2023-01-13", interval='5m')
data.iloc[:,:]
data.Open.iloc