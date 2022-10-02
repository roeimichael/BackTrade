import time
import concurrent.futures
import numpy as np
import talib
import pandas as pd
import datesEdit as of
import pandas_ta as ta
from warnings import simplefilter
from os import listdir
from os.path import isfile, join
import yfinance as yf

START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'
PERIOD = "3y"
WINDOWSIZE = 10

if __name__ == '__main__':
    # stock = yf.Ticker('ANTM')
    # df = stock.history(start=START, end=END, interval=INTERVAL, prepost=False)
    # df = df.drop(columns=['Stock Splits'])
    # print(df)
