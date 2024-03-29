import pandas as pd
import time
import numpy as np

WINDOWSIZE = 100
not_normalized = ["ma200", "ma50", "TRIX", "stochK", "stochD", "TRANGE", "BBupperband", "BBmiddleband", "BBlowerband",
                  "ao", "cci", "coppock", "mom", "pgo", "alma", "dema", "wma", "fwma", "hma", "hwma", "jma", "kama",
                  "mcgd", "pwma", "sinwma", "swma", "tema", "trima", "t3", "vidya", "vwma", "zlma", "qstick", "vhf",
                  "atr", "massi", "pdist", "rvi", "ui", "ad", "adosc", "cmf", "efi", "obv", "pvt", "Market Cap", "DPC",
                  "Cumulative Return"]
normalized = ["ADX", "ADXR", "AROONOSC", "DX", "PPO", "ULTOSC", "MACD", "MACDSIG", "MACDHIS", "apo", "bias", "bop",
              "cfo", "cmo", "cti", "inertia", "psl", "roc", "rsi", "rsx", "willr", "chop", "increasing", "decreasing",
              "mfi", "pvr", "ebsw", "PriceUp", "PriceDown", "VIX", "VVIX", "VXN"]

not_normalized_small = ["ma50", "ma200", "TRIX", "stochK", "stochD", "TRANGE", "BBupperband", "BBmiddleband",
                        "BBlowerband","cci", "mom","wma",  "tema", "atr", "rvi", "Market Cap", "DPC", "Cumulative Return"]


# input: list of unnormalized column.
# output: list of normalized column.
# a normalization method that is similar to the normal distribution normalization only that this method uses a
# window that moves along the cell currently normalized and the values calculated to normalized are taken from the
# cells in the window after the current cell

def windownormdist_normalization(list):
    normalized_data, sublist = [], []
    for i in range(len(list) - WINDOWSIZE):
        sublist = list[i:i + WINDOWSIZE]
        m = np.mean(sublist, axis=0)
        std = np.std(sublist, axis=0)
        normalized_data.append((list[i] - m) / std)
    for j in range(WINDOWSIZE):
        normalized_data.append(None)
    return normalized_data


# input: list of unnormalized column.
# output: list of normalized column.
# a normalization method that takes into account the tanh of the current cell value compared to others in the column.
# it is a pretty accurate normalization model.
def tanh_normalization(unnormalized_data):
    m = np.mean(unnormalized_data, axis=0)
    std = np.std(unnormalized_data, axis=0)
    normalized_data = 0.5 * (np.tanh(0.01 * ((unnormalized_data - m) / std)) + 1)
    return normalized_data


# input: list of unnormalized column.
# output: list of normalized column.
# the normal distribution model is probably the most popular. it takes the mean and the standard deviation of the
# column and normalize each cell by them.
def normdist_normalization(unnormalized_data_1):
    m = np.nanmean(unnormalized_data_1)
    std = np.nanstd(unnormalized_data_1)
    normalized_data = (unnormalized_data_1 - m) / std
    return normalized_data


# input: list of unnormalized column.
# output: list of normalized column.
# sigmoid normalization takes the sigmoid function 1/(1+e^-x) and outputs the normalized column back with values
# between 0 and 1 depending on the strength of the input data to the function.
def sigmoid_normalization(unnormalized_data):
    normalized_data = []
    for x in unnormalized_data:
        normalized_data.append(1 / (1 + np.exp(-x)))
    return normalized_data


# input: list of unnormalized column.
# output: list of normalized column.
# median normalization takes into a count only the median of the entered data and normalize it by deviding each cell
# by it. not so accurate and probably will only used experimentally
def median_normalization(unnormalized_data):
    m = np.median(unnormalized_data, axis=0)
    normalized_data = unnormalized_data / m
    return normalized_data


# input: list of unnormalized column.
# output: list of normalized column.
# min max normalization is also a very popular method the one i created output values between 0 and 1 wheh the
# highest value in the input column will return as one and vise versa for the lowest value as 0. the model is pretty
# accurate and will be used in the future.
def min_max_normalization(unnormalized_data):
    normalized_data = (unnormalized_data - min(unnormalized_data)) / (max(unnormalized_data) - min(unnormalized_data))
    return normalized_data


# input: list of tickers.
# output: none.
# the main function of the file which takes every ticker file and run on every unnormalized column and normalize it
# with the aforementioned normalization method.
def normalize_tickers(tickers):
    print("normalizing all stocks dfs...")
    unavilable = []
    for index, ticker in enumerate(tickers):
        try:
            print(f"currently at {index + 1} stock {ticker} out of {len(tickers)}")
            df = pd.read_csv(f"./data/stocks/{ticker}.csv")
            for column in not_normalized_small:
                unnormalized_data = df[f'{column}'].tolist()
                normalized_data = windownormdist_normalization(unnormalized_data)
                df[f'{column}'] = normalized_data
            df = df.iloc[:-WINDOWSIZE, :]
            df.to_csv(f"./data/stocks/{ticker}.csv")
        except:
            unavilable.append(ticker)
    print(unavilable)


# input: list of tickers. output: none. defualt main function to run the funcions and measure time (right now only
# runs one function but created incase other functiuons will be needed).
def normalization_main(tickers):
    t1 = time.perf_counter()
    normalize_tickers(tickers)
    t2 = time.perf_counter()
    print(f'Finished normalization_main in {t2 - t1} seconds')
