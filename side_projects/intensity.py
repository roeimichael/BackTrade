import yfinance as yf
import pandas as pd
import time
import matplotlib.pyplot as plt

def get_tickers():
    ticks = []
    f = open("S&P 500.txt", "r")
    list_of_tickers = f.read().split(",")
    for ticker in list_of_tickers:
        ticks.append(ticker.split(":")[1])
    return ticks


if __name__ == '__main__':
    t1 = time.perf_counter()
    tot_volume = 0
    tickers = get_tickers()

    data = yf.download(tickers, '2019-1-1')['Volume']
    snoopy = yf.download('SPY', '2019-1-1')
    snoopy = snoopy.drop(columns=['High', 'Low', 'Adj Close', 'Volume'])
    snoopy['delta'] = snoopy['Close'] - snoopy['Open']
    data['sum'] = data[tickers].astype(float).sum(axis=1)
    df = pd.concat([data, snoopy], axis=1, join='inner')
    df['intensity'] = (df['delta'] * df['sum'])/2
    # df.to_csv('intensity.csv')
    df['intensity'].plot()
    plt.ylabel('intensity')
    plt.xlabel('time')
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')

