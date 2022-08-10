import time
import concurrent.futures
import yfinance as yf
import numpy as np
import talib
import pandas as pd
import pandas_ta as ta
from warnings import simplefilter
from os import listdir
from os.path import isfile, join

START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'
PERIOD = "3y"
SPLITS = 25
TARGET_THREASHOLD = 0.025

# removes warnings
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
simplefilter(action='ignore', category=FutureWarning)
# takes a list of all candle names
candle_names = talib.get_function_groups()['Pattern Recognition']

# creates values of the VIX,VVIX and VXN so that they could be added to the stock information as a breath market
# indicator.
vix = yf.Ticker('^VIX')
vix = vix.history(start=START, end=END, interval=INTERVAL)
vvix = yf.Ticker('^VVIX')
vvix = vvix.history(start=START, end=END, interval=INTERVAL)
vxn = yf.Ticker('^VXN')
vxn = vxn.history(start=START, end=END, interval=INTERVAL)


# adds all the candles to the data
def add_candles(df):
    for candle in candle_names:
        df[candle] = getattr(talib, candle)(df['Open'], df['High'], df['Low'], df['Close'])


# adds all the technical indicators to the data (taken from talib and pandas_ta)
def add_indicators(df):
    df['ma50'] = df['Open'].rolling(50).mean()
    df['ma200'] = df['Open'].rolling(200).mean()
    df['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['ADXR'] = talib.ADXR(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['AROONOSC'] = talib.AROONOSC(df['High'], df['Low'], timeperiod=14)
    df['DX'] = talib.DX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['PPO'] = talib.PPO(df['Close'], fastperiod=12, slowperiod=26)
    df['stochK'], df['stochD'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3,
                                             slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['TRIX'] = talib.TRIX(df['Close'], timeperiod=14)
    df['ULTOSC'] = talib.ULTOSC(df['High'], df['Low'], df['Close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
    df['MACD'], df['MACDSIG'], df[' MACDHIST'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['TRANGE'] = talib.TRANGE(df['High'], df['Low'], df['Close'])
    df['BBupperband'], df['BBmiddleband'], df['BBlowerband'] = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2,
                                                                            nbdevdn=2, matype=0)
    indicators = [df.ta.ao(), df.ta.apo(), df.ta.bias(), df.ta.bop(), df.ta.cci(), df.ta.cfo(), df.ta.cmo(),
                  df.ta.coppock(), df.ta.cti(), df.ta.inertia(), df.ta.mom(), df.ta.pgo(), df.ta.psl(), df.ta.roc(),
                  df.ta.rsi(), df.ta.rsx(), df.ta.willr(), df.ta.alma(), df.ta.dema(),
                  df.ta.wma(), df.ta.fwma(), df.ta.hma(), df.ta.hwma(), df.ta.jma(), df.ta.kama(),
                  df.ta.mcgd(), df.ta.pwma(), df.ta.sinwma(), df.ta.swma(), df.ta.t3(),
                  df.ta.tema(), df.ta.trima(), df.ta.vidya(), df.ta.vwma(), df.ta.zlma(), df.ta.chop(),
                  df.ta.increasing(), df.ta.decreasing(), df.ta.qstick(), df.ta.vhf(), df.ta.atr(),
                  df.ta.massi(), df.ta.pdist(), df.ta.rvi(), df.ta.ui(), df.ta.ad(), df.ta.adosc(),
                  df.ta.cmf(), df.ta.efi(), df.ta.mfi(), df.ta.obv(), df.ta.pvr(), df.ta.pvt(),
                  df.ta.ebsw()]
    names = ['ao', 'apo', 'bias', 'bop', 'cci', 'cfo', 'cmo', 'coppock', 'cti', 'inertia', 'mom', 'pgo', 'psl',
             'roc', 'rsi', 'rsx', 'willr', 'alma', 'dema', 'wma', 'fwma', 'hma', 'hwma', 'jma', 'kama',
             'mcgd', 'pwma', 'sinwma', 'swma', 't3', 'tema', 'trima', 'vidya', 'vwma', 'zlma', 'chop',
             'increasing', 'decreasing', 'qstick', 'vhf', 'atr', 'massi', 'pdist', 'rvi',
             'ui', 'ad', 'adosc', 'cmf', 'efi', 'mfi', 'obv', 'pvr', 'pvt', 'ebsw', ]

    for name, indicator in zip(names, indicators):
        try:
            df[name] = indicator
        except:
            print(f"the problame is in indicator : {indicator}, {name}")


# adds other types of information to the data, and the target column.
def add_other(df):
    df['VIX'] = vix['Close']
    df['VVIX'] = vvix['Close']
    df['VXN'] = vxn['Close']
    df['Market Cap'] = df['Open'] * df['Volume']
    df['DPC'] = df['Open'] / df['Open'].shift(1) - 1
    df['Cumulative Return'] = (1 + df['DPC']).cumprod()
    df['PriceUp'] = np.where(df['DPC'] > 0, 1, 0)
    df['PriceDown'] = np.where(df['DPC'] < 0, 1, 0)
    df['Close Change'] = df['Close'] / df['Close'].shift(1) - 1
    df['Target'] = np.where(df['Close Change'] > TARGET_THREASHOLD, 1, 0)


# a support function created to see if all the files are in place.
def check_data(tickers):
    onlyfiles = [f for f in listdir("./data/stocks/") if isfile(join("./data/stocks/", f))]
    print(len(onlyfiles))
    print(len(tickers))


# creates the thread for the scanner to run on
def create_threads(splits):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(create_csv, splits)


# creats each individual csv and call the data filling functions for that stock.
def create_csv(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(start=START, end=END, interval=INTERVAL, prepost=False)
    df = df.drop(columns=['Stock Splits'])
    df.insert(0, 'ticker', ticker)
    add_candles(df)
    add_indicators(df)
    add_other(df)
    df.to_csv(f"./data/stocks/{ticker}.csv")


# creates multiprocesses for the data to be divided on and each multiproccess is than being divided to threads and on
# each thread a stock file is being created.
def main(tickers):
    t1 = time.perf_counter()
    splits = np.array_split(tickers, SPLITS)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(create_threads, splits)
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')



