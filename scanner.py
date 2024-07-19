import time
import talib
import numpy as np
import pandas as pd
import yfinance as yf
from os import listdir
import concurrent.futures
from os.path import isfile, join
from warnings import simplefilter

# Constants
START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'
PERIOD = "3y"
SPLITS = 25
TARGET_THRESHOLD = 0.02

# Suppress warnings
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
simplefilter(action='ignore', category=FutureWarning)

# List of candle patterns from TA-Lib
candle_names = talib.get_function_groups()['Pattern Recognition']

# Fetch VIX and VXN data
vix = yf.Ticker('^VIX').history(start=START, end=END, interval=INTERVAL)
vxn = yf.Ticker('^VXN').history(start=START, end=END, interval=INTERVAL)


def add_candles(df):
    """
    Add candle pattern recognition indicators to DataFrame.
    """
    for candle in candle_names:
        df[candle] = getattr(talib, candle)(df['Open'], df['High'], df['Low'], df['Close'])


def add_indicators(df):
    """
    Add technical indicators to DataFrame using TA-Lib and pandas_ta.
    """
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
    df['MACD'], df['MACDSIG'], df['MACDHIST'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['TRANGE'] = talib.TRANGE(df['High'], df['Low'], df['Close'])
    df['BBupperband'], df['BBmiddleband'], df['BBlowerband'] = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2,
                                                                            nbdevdn=2, matype=0)

    # Add additional indicators from pandas_ta
    indicators = [
        df.ta.ao(), df.ta.apo(), df.ta.bias(), df.ta.bop(), df.ta.cci(), df.ta.cfo(), df.ta.cmo(),
        df.ta.coppock(), df.ta.cti(), df.ta.inertia(), df.ta.mom(), df.ta.pgo(), df.ta.psl(), df.ta.roc(),
        df.ta.rsi(), df.ta.rsx(), df.ta.willr(), df.ta.alma(), df.ta.dema(), df.ta.wma(), df.ta.fwma(),
        df.ta.hma(), df.ta.hwma(), df.ta.jma(), df.ta.kama(), df.ta.pwma(), df.ta.sinwma(), df.ta.swma(),
        df.ta.t3(), df.ta.tema(), df.ta.trima(), df.ta.vwma(), df.ta.zlma(), df.ta.chop(), df.ta.increasing(),
        df.ta.decreasing(), df.ta.qstick(), df.ta.vhf(), df.ta.atr(), df.ta.massi(), df.ta.pdist(), df.ta.rvi(),
        df.ta.ui(), df.ta.ad(), df.ta.adosc(), df.ta.cmf(), df.ta.efi(), df.ta.mfi(), df.ta.obv(), df.ta.pvr(),
        df.ta.pvt(), df.ta.ebsw()
    ]

    indicator_names = [
        'ao', 'apo', 'bias', 'bop', 'cci', 'cfo', 'cmo', 'coppock', 'cti', 'inertia', 'mom', 'pgo', 'psl', 'roc',
        'rsi', 'rsx', 'willr', 'alma', 'dema', 'wma', 'fwma', 'hma', 'hwma', 'jma', 'kama', 'pwma', 'sinwma',
        'swma', 't3', 'tema', 'trima', 'vwma', 'zlma', 'chop', 'increasing', 'decreasing', 'qstick', 'vhf', 'atr',
        'massi', 'pdist', 'rvi', 'ui', 'ad', 'adosc', 'cmf', 'efi', 'mfi', 'obv', 'pvr', 'pvt', 'ebsw'
    ]

    for name, indicator in zip(indicator_names, indicators):
        try:
            df[name] = indicator
        except Exception as e:
            print(f"Problem with indicator: {name}, {indicator} - {e}")


def add_part_ind(df):
    """
    Add a subset of technical indicators to DataFrame.
    """
    df['ma50'] = df['Open'].rolling(50).mean()
    df['ma200'] = df['Open'].rolling(200).mean()
    df['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['ADXR'] = talib.ADXR(df['High'], df['Low'], df['Close'], timeperiod=14)
    df['AROONOSC'] = talib.AROONOSC(df['High'], df['Low'], timeperiod=14)
    df['stochK'], df['stochD'] = talib.STOCH(df['High'], df['Low'], df['Close'], fastk_period=5, slowk_period=3,
                                             slowk_matype=0, slowd_period=3, slowd_matype=0)
    df['TRIX'] = talib.TRIX(df['Close'], timeperiod=14)
    df['ULTOSC'] = talib.ULTOSC(df['High'], df['Low'], df['Close'], timeperiod1=7, timeperiod2=14, timeperiod3=28)
    df['MACD'], df['MACDSIG'], df['MACDHIST'] = talib.MACD(df['Close'], fastperiod=12, slowperiod=26, signalperiod=9)
    df['TRANGE'] = talib.TRANGE(df['High'], df['Low'], df['Close'])
    df['BBupperband'], df['BBmiddleband'], df['BBlowerband'] = talib.BBANDS(df['Close'], timeperiod=5, nbdevup=2,
                                                                            nbdevdn=2, matype=0)

    indicators = [
        df.ta.apo(), df.ta.cci(), df.ta.cfo(), df.ta.cmo(), df.ta.cti(), df.ta.mom(), df.ta.roc(), df.ta.rsi(),
        df.ta.rsx(), df.ta.willr(), df.ta.wma(), df.ta.tema(), df.ta.atr(), df.ta.rvi()
    ]

    indicator_names = [
        'apo', 'cci', 'cfo', 'cmo', 'cti', 'mom', 'roc', 'rsi', 'rsx', 'willr', 'wma', 'tema', 'atr', 'rvi'
    ]

    for name, indicator in zip(indicator_names, indicators):
        try:
            df[name] = indicator
        except Exception as e:
            print(f"Problem with indicator: {name}, {indicator} - {e}")


def add_other(df):
    """
    Add additional market data and target column to DataFrame.
    """
    df['VIX'] = vix['Close']
    df['VXN'] = vxn['Close']
    df['Market Cap'] = df['Open'] * df['Volume']
    df['DPC'] = df['Open'] / df['Open'].shift(1) - 1
    df['Cumulative Return'] = (1 + df['DPC']).cumprod()
    df['PriceUp'] = np.where(df['DPC'] > 0, 1, -1)
    df['Close Change'] = df['Close'] / df['Close'].shift(1) - 1
    df['Open Change'] = df['Open'] / df['Open'].shift(1) - 1
    df['High Change'] = df['High'] / df['High'].shift(1) - 1
    df['Low Change'] = df['Low'] / df['Low'].shift(1) - 1
    df['Target'] = np.where(df['Close Change'] > TARGET_THRESHOLD, 1, 0)


def check_data(tickers):
    """
    Check if all stock data files are present.
    """
    onlyfiles = [f for f in listdir("./data_new/stocks/") if isfile(join("./data_new/stocks/", f))]
    print(f"Files found: {len(onlyfiles)}, Tickers count: {len(tickers)}")


def create_threads(splits):
    """
    Create threads for concurrent processing.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(create_csv, splits)


def create_csv(ticker):
    """
    Create a CSV file for each ticker with processed data.
    """
    stock = yf.Ticker(ticker)
    df = stock.history(start=START, end=END, interval=INTERVAL, prepost=False)
    df.drop(columns=['Stock Splits', 'Dividends'], inplace=True)
    df.insert(0, 'ticker', ticker)
    add_part_ind(df)
    add_other(df)
    df.drop(['Close', 'Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)
    df.to_csv(f"./data_new/stocks/{ticker}.csv")


def main(tickers):
    t1 = time.perf_counter()
    print("Creating basic files...")
    splits = np.array_split(tickers, SPLITS)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(create_threads, splits)
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')


if __name__ == '__main__':
    # Example usage
    # tickers = get_tickers()  # Assuming you have a function to get tickers
    # main(tickers)
    pass
