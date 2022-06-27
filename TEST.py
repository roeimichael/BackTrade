import time
import concurrent.futures
import yfinance as yf
import numpy as np
import talib
import pandas as pd
import otherfunctions as of
import pandas_ta as ta
from warnings import simplefilter
from os import listdir
from os.path import isfile, join

START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'
PERIOD = "3y"
SPLITS = 25
stock = yf.Ticker('MSFT')
df = stock.history(start=START, end=END, interval=INTERVAL, prepost=False)
mfi = talib.MFI(df['High'], df['Low'], df["Close"], df['Volume'], timeperiod=14)
mfi2 = df.ta.mfi()
roc = talib.ROC( df["Close"], timeperiod=10)
roc2 = df.ta.roc()
rsi = talib.RSI( df["Close"], timeperiod=14)
rsi2 = df.ta.rsi()
trima = talib.TRIMA( df["Close"], timeperiod=30)
trima2 = df.ta.trima()
atr = talib.ATR(df['High'], df['Low'], df["Close"], timeperiod=14)
atr2= df.ta.vhf()

print(atr2)
