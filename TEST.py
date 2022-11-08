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
    tickers = []
    with open('./data/tickers.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            tickers.append(x)
    tickers.append('^GSPC')
    data = yf.download(tickers[:100], end='2022-01-01', start='2017-01-01', interval='1mo')['Adj Close']


    print(data.head(10))
    # log_returns = np.log(data / data.shift())
    # cov = log_returns.cov()
    # var = log_returns['^GSPC'].var()
    # for tick in tickers:
    #     print(f"{cov.loc[tick, '^GSPC'] / var} is b for {tick}")
