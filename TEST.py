import time
import concurrent.futures
from pandas_ta import *
import yfinance as yf

import pandas as pd
from warnings import simplefilter
from os import listdir
from os.path import isfile, join


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
    vvix = yf.Ticker('^VVIX')
    vvix = vvix.history(start=START, end=END, interval=INTERVAL)


    print(vvix.head(455))
    # log_returns = np.log(data / data.shift())
    # cov = log_returns.cov()
    # var = log_returns['^GSPC'].var()
    # for tick in tickers:
    #     print(f"{cov.loc[tick, '^GSPC'] / var} is b for {tick}")
