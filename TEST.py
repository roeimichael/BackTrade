import time
import concurrent.futures
import yfinance as yf
import numpy as np
import talib
import pandas as pd
import datesEdit as of
import pandas_ta as ta
from warnings import simplefilter
from os import listdir
from os.path import isfile, join

WINDOWSIZE = 10
not_normalized = ["hwma", "jma", "kama", "mcgd", "pwma", "sinwma", "swma", "t3", "tema", "trima", "vidya", "vwma", "zlma", "qstick", "vhf",
                  "atr", "massi", "pdist", "rvi", "ui", "ad", "adosc", "cmf", "efi", "obv", "pvt", "Market Cap", "DPC",
                  "Cumulative Return"]
START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'


def perchange (ticker,start_date,end_date):
    stock = yf.Ticker(ticker)
    df_sp = stock.history(start=START, end=END, interval=INTERVAL)
    df['Open Change'] = df['Open'] / df['Open'].shift(1) - 1
    df['Close Change'] = df['Close'] / df['Close'].shift(1) - 1
    df['PriceUp'] = np.where(df['DPC'] > 0, 1, 0)
    df['PriceDown'] = np.where(df['DPC'] < 0, 1, 0)

def windownormdist_normalization(list):
    normalized_data,sublist = [],[]
    m, std = 0,0
    for i in range(len(list) - WINDOWSIZE):
        sublist = list[i:i + WINDOWSIZE]
        m = np.mean(sublist, axis=0)
        std = np.std(sublist, axis=0)
        normalized_data.append((list[i] - m) / std)
    for j in range(WINDOWSIZE):
        normalized_data.append((list[j-10] - m) / std)
    return normalized_data


if __name__ == '__main__':
    df = pd.read_csv(f"./data/stocks/AAPL_NOTNORM.csv")
    for column in not_normalized:
        unnormalized_data = df[f'{column}'].tolist()
        normalized_data = windownormdist_normalization(unnormalized_data)
        df[f'{column}'] = normalized_data
