import time
import talib
import numpy as np
import pandas as pd
import yfinance as yf
from os import listdir
import concurrent.futures
from os.path import isfile, join
from warnings import simplefilter

from config.data_config import DataConfig
from config.processing_config import ProcessingConfig
from config.path_config import PathConfig
from utils.indicator_utils import add_talib_indicators, add_pandas_ta_indicators

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
simplefilter(action='ignore', category=FutureWarning)

candle_names = talib.get_function_groups()['Pattern Recognition']

vix = yf.Ticker(DataConfig.VIX_TICKER).history(
    start=DataConfig.START_DATE,
    end=DataConfig.END_DATE,
    interval=DataConfig.INTERVAL
)
vxn = yf.Ticker(DataConfig.VXN_TICKER).history(
    start=DataConfig.START_DATE,
    end=DataConfig.END_DATE,
    interval=DataConfig.INTERVAL
)


def add_candles(df):
    for candle in candle_names:
        df[candle] = getattr(talib, candle)(df['Open'], df['High'], df['Low'], df['Close'])


def add_other_features(df):
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
    df['Target'] = np.where(df['Close Change'] > ProcessingConfig.TARGET_THRESHOLD, 1, 0)


def check_data(tickers):
    stocks_dir = str(PathConfig.DATA_NEW_STOCKS_DIR)
    onlyfiles = [f for f in listdir(stocks_dir) if isfile(join(stocks_dir, f))]
    print(f"Files found: {len(onlyfiles)}, Tickers count: {len(tickers)}")


def create_threads(splits):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(create_csv, splits)


def create_csv(ticker):
    stock = yf.Ticker(ticker)
    df = stock.history(
        start=DataConfig.START_DATE,
        end=DataConfig.END_DATE,
        interval=DataConfig.INTERVAL,
        prepost=False
    )
    df.drop(columns=['Stock Splits', 'Dividends'], inplace=True)
    df.insert(0, 'ticker', ticker)

    add_talib_indicators(df, subset=True)
    add_pandas_ta_indicators(df, subset=True)
    add_other_features(df)

    df.drop(['Close', 'Open', 'High', 'Low', 'Volume'], axis=1, inplace=True)
    output_path = PathConfig.DATA_NEW_STOCKS_DIR / f"{ticker}.csv"
    df.to_csv(output_path)


def main(tickers):
    t1 = time.perf_counter()
    print("Creating basic files...")
    splits = np.array_split(tickers, ProcessingConfig.SPLITS)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(create_threads, splits)
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1:.2f} seconds')


if __name__ == '__main__':
    pass
