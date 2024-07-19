import time
import pandas as pd
import numpy as np

# Constants
WINDOWSIZE = 100
NOT_NORMALIZED = [
    "ma200", "ma50", "TRIX", "stochK", "stochD", "TRANGE", "BBupperband", "BBmiddleband", "BBlowerband",
    "ao", "cci", "coppock", "mom", "pgo", "alma", "dema", "wma", "fwma", "hma", "hwma", "jma", "kama",
    "mcgd", "pwma", "sinwma", "swma", "tema", "trima", "t3", "vidya", "vwma", "zlma", "qstick", "vhf",
    "atr", "massi", "pdist", "rvi", "ui", "ad", "adosc", "cmf", "efi", "obv", "pvt", "Market Cap", "DPC",
    "Cumulative Return"
]
NORMALIZED = [
    "ADX", "ADXR", "AROONOSC", "DX", "PPO", "ULTOSC", "MACD", "MACDSIG", "MACDHIS", "apo", "bias", "bop",
    "cfo", "cmo", "cti", "inertia", "psl", "roc", "rsi", "rsx", "willr", "chop", "increasing", "decreasing",
    "mfi", "pvr", "ebsw", "PriceUp", "PriceDown", "VIX", "VVIX", "VXN"
]
NOT_NORMALIZED_SMALL = [
    "ma50", "ma200", "TRIX", "stochK", "stochD", "TRANGE", "BBupperband", "BBmiddleband", "BBlowerband",
    "cci", "mom", "wma", "tema", "atr", "rvi", "Market Cap", "DPC", "Cumulative Return"
]


def windownormdist_normalization(data):
    normalized_data = []
    for i in range(len(data) - WINDOWSIZE):
        sublist = data[i:i + WINDOWSIZE]
        m = np.mean(sublist)
        std = np.std(sublist)
        normalized_data.append((data[i] - m) / std)
    normalized_data.extend([None] * WINDOWSIZE)
    return normalized_data


def tanh_normalization(data):
    m = np.mean(data)
    std = np.std(data)
    return 0.5 * (np.tanh(0.01 * ((data - m) / std)) + 1)


def normdist_normalization(data):
    m = np.nanmean(data)
    std = np.nanstd(data)
    return (data - m) / std


def sigmoid_normalization(data):
    return [1 / (1 + np.exp(-x)) for x in data]


def median_normalization(data):
    m = np.median(data)
    return data / m


def min_max_normalization(data):
    return (data - min(data)) / (max(data) - min(data))


def normalize_tickers(tickers):
    print("Normalizing all stock dataframes...")
    unavailable = []
    for index, ticker in enumerate(tickers):
        try:
            print(f"Currently processing {index + 1} of {len(tickers)}: {ticker}")
            df = pd.read_csv(f"./data/stocks/{ticker}.csv")
            for column in NOT_NORMALIZED_SMALL:
                unnormalized_data = df[column].tolist()
                normalized_data = windownormdist_normalization(unnormalized_data)
                df[column] = normalized_data
            df = df.iloc[:-WINDOWSIZE, :]
            df.to_csv(f"./data/stocks/{ticker}.csv", index=False)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            unavailable.append(ticker)
    if unavailable:
        print(f"Unavailable tickers: {unavailable}")


def normalization_main(tickers):
    t1 = time.perf_counter()
    normalize_tickers(tickers)
    t2 = time.perf_counter()
    print(f'Finished normalization_main in {t2 - t1:.2f} seconds')

