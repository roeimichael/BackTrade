import pandas as pd
import time
import datesEdit as of
import numpy as np

WINDOWSIZE = 100
not_normalized = ["ma200", "ma50", "TRIX", "stochK", "stochD", "TRANGE", "BBupperband", "BBmiddleband", "BBlowerband",
                  "ao", "cci", "coppock", "mom", "pgo", "alma", "dema", "wma", "fwma", "hma", "hwma", "jma", "kama",
                  "mcgd", "pwma", "sinwma", "swma", "t3", "tema", "trima", "vidya", "vwma", "zlma", "qstick", "vhf",
                  "atr", "massi", "pdist", "rvi", "ui", "ad", "adosc", "cmf", "efi", "obv", "pvt", "Market Cap", "DPC",
                  "Cumulative Return"]
normalized = ["ADX", "ADXR", "AROONOSC", "DX", "PPO", "ULTOSC", "MACD", "MACDSIG", "MACDHIS", "apo", "bias", "bop",
              "cfo", "cmo", "cti", "inertia", "psl", "roc", "rsi", "rsx", "willr", "chop", "increasing", "decreasing",
              "mfi", "pvr", "ebsw", "PriceUp", "PriceDown", "VIX", "VVIX", "VXN"]


# a normalization method that is similar to the noremal distribution normalization only that this method uses a
# window that moves along the cell currently normalized and the values caclulated to normalized are taken from the
# cells in the windfow after the currenct cell

def windownormdist_normalization(list):
    normalized_data, sublist = [], []
    m, std = 0, 0
    for i in range(len(list) - WINDOWSIZE):
        sublist = list[i:i + WINDOWSIZE]
        m = np.mean(sublist, axis=0)
        std = np.std(sublist, axis=0)
        normalized_data.append((list[i] - m) / std)
    for j in range(WINDOWSIZE):
        normalized_data.append((list[j - 10] - m) / std)
    return normalized_data


# a normalization method that takes into account the tanh of the current cell value compared to others in the column.
# it is a pretty accurate normalization model.
def tanh_normalization(unnormalized_data):
    m = np.mean(unnormalized_data, axis=0)
    std = np.std(unnormalized_data, axis=0)
    normalized_data = 0.5 * (np.tanh(0.01 * ((unnormalized_data - m) / std)) + 1)
    return normalized_data


# the normal distribution model is probably the most popular. it takes the mean and the standard deviation of the
# column and normalize each cell by them.
def normdist_normalization(unnormalized_data):
    m = np.mean(unnormalized_data, axis=0)
    std = np.std(unnormalized_data, axis=0)
    normalized_data = (unnormalized_data - m) / std
    return normalized_data


# sigmoid normalization takes the sigmoid function 1/(1+e^-x) and outputs the normalized column back with values
# between 0 and 1 depending on the strength of the input data to the function.
def sigmoid_normalization(unnormalized_data):
    normalized_data = []
    for x in unnormalized_data:
        normalized_data.append(1 / (1 + np.exp(-x)))
    return normalized_data


# median normalization takes into a count only the median of the entered data and normalize it by deviding each cell
# by it. not so accurate and probably will only used experimentally
def median_normalization(unnormalized_data):
    m = np.median(unnormalized_data, axis=0)
    normalized_data = unnormalized_data / m
    return normalized_data


# min max normalization is also a very popular method the one i created output values between 0 and 1 wheh the
# highest value in the input column will return as one and vise versa for the lowest value as 0. the model is pretty
# accurate and will be used in the future.
def min_max_normalization(unnormalized_data):
    normalized_data = (unnormalized_data - min(unnormalized_data)) / (max(unnormalized_data) - min(unnormalized_data))
    return normalized_data


# the main function of the file which takes every ticker file and run on every unnormalized column and normalize it
# with the aforementioned normalization method.
def normalize_tickers(tickers):
    unavilable = []
    for index, ticker in enumerate(tickers):
        try:
            print(f"currently at {index + 1} out of {len(tickers)}")
            df = pd.read_csv(f"./data/stocks/{ticker}.csv")
            for column in not_normalized:
                unnormalized_data = df[f'{column}'].tolist()
                normalized_data = windownormdist_normalization(unnormalized_data)
                df[f'{column}'] = normalized_data
            df.to_csv(f"./data/stocks/{ticker}.csv")
        except:
            unavilable.append(ticker)
    print(unavilable)


# defualt main function to run the functions required as one.
def normalization_main():
    t1 = time.perf_counter()
    tickers = of.get_tickers()
    # dates = of.get_dates(tickers)
    normalize_tickers(tickers)
    t2 = time.perf_counter()
    print(f'Finished normalization_main in {t2 - t1} seconds')
