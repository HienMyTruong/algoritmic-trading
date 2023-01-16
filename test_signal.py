import yfinance as yf
import pandas as pd
import numpy as np

data = yf.download("EURUSD=X", start="2023-01-01", end="2023-01-13", interval='5m')
data.iloc[:,:]
#print(data.Open.iloc[-1])

def signal_generator(dataframe):
    open = dataframe.Open.iloc[-1]
    close = dataframe.Close.iloc[-1]
    previous_open = dataframe.Open.iloc[-2]
    previous_close = dataframe.Close.iloc[-2]

    #Bearish Pattern
    if(open>close and previous_open<previous_close and open>=previous_close):
        return 1

    #Bullish Pattern
    elif(open<close and previous_open>previous_close and close>previous_open and open<=previous_close):
        return 2

    else:
        return 0

signal = []

signal.append(0)

for i in range(1, len(data)):
    df = data[i-1:i+1]
    signal.append(signal_generator(df))
data["signal"] = signal

print(data.iloc[:,:])
print(data.signal.value_counts())

data.to_csv(r'/Users/hientruong/PycharmProjects/algoritmic-trading/saved_data/data.csv', index=False, header=True)




