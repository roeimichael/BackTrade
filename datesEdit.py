import pandas as pd
import yfinance as yf
import time
import pandas_ta as ta
import glob

START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'
PERIOD = "3y"
SNPPATH = "S&P500.csv"
path = "c:/users/roeym/desktop/backtrade/data/dates/*.csv"


# input: list of dates , S&P tickers file.
# output: none.
# calculate the stocks that went up compared to the ones that went down at every day and than adds it as a column to
# the data values.
def get_advance_decline_ratio(dates, df_sp):
    print("calculating advance decline ratio...")
    adr, add = [], []
    for date in dates:
        date_df = pd.read_csv(f"./data/dates/{date}.csv")
        advance = (date_df['PriceUp'] == 1).sum()
        decline = (date_df['PriceDown'] == 1).sum()
        if decline == 0:
            decline = 0.0000000000001
        ad_ratio = advance / decline
        ad_difference = advance - decline
        date_df['AD_difference'] = ad_difference
        date_df['AD_RATIO'] = ad_ratio
        date_df.to_csv(f"./data/dates/{date}.csv")
        add.append(ad_difference)
        adr.append(ad_ratio)
    df_sp['AD_difference'] = add
    df_sp['AD_ratio'] = adr
    df_sp.to_csv(SNPPATH)


# input: list of dates.
# output: none.
# after the A/D ratio is calculated the mcclelan osc is an breath market indicator that takes into account moving
# averages of the AD raio and generage a general picture of the market.
def calc_mcclellan(dates):
    print("calculating mcclellan indicator...")
    df = pd.read_csv(SNPPATH, index_col=[0])
    add = df['AD_difference']
    ema19 = ta.ema((add * 0.1), 19)
    ema39 = ta.ema((add * 0.05), 39)
    mcclellanosc = ema19 - ema39
    df['mcclellanOSC'] = mcclellanosc
    mcclellansum = mcclellanosc.cumsum()
    df['mcclellanSUM'] = mcclellansum
    df.to_csv(SNPPATH)
    for index, date in enumerate(dates):
        if index >= 38:
            curr_df = pd.read_csv(f"./data/dates/{date}.csv")
            curr_df['mcclellanSUM'] = mcclellansum[index]
            curr_df['mcclellanOSC'] = mcclellanosc[index]
            curr_df.to_csv(f"./data/dates/{date}.csv")


# input: list of all the tickers, and a specific ticker.
# output: list of 3 tickers.
# the function calculates the top 3 highest correlated tickers to the specific one inserted and returns them.
def get_high_corr(ticker, tickers):
    req_df = pd.read_csv(f"./data/stocks/{ticker}.csv")
    req_close = req_df['Close']
    corr = []
    tickers.remove(ticker)
    for stock in tickers:
        test_df = pd.read_csv(f"./data/stocks/{stock}.csv")
        test_close = test_df['Close']
        corr.append(test_close.corr(req_close))
    top3 = sorted(zip(corr, tickers), reverse=True)[:3]
    return [x[1] for x in top3]


# input: list of dates, list of columns (data columns).
# output: none.
# the function creates all the empty dates files.
def creating_dates(dates, columns):
    print("creating dates files...")
    for date in dates:
        df = pd.DataFrame(columns=columns)
        df.to_csv(f"./data/dates/{date}.csv")


# input: list of dates, list of tickers.
# output: none.
# converts all the stocks that were already built and normalized and transfer each attribute in the stock file to all
# 758 dates, loops through all the stocks and divides them up to all the dates.
def stocks_to_dates(tickers, dates):
    print("moving from stocks to dates files...")
    bad_stocks = []
    for index, ticker in enumerate(tickers):
        try:
            print(f"currently at {index + 1} stock {ticker} out of {len(tickers)}")
            ticker_df = pd.read_csv(f"./data/stocks/{ticker}.csv")
            for date in dates:
                curr_date_df = pd.read_csv(f"./data/dates/{date}.csv", index_col=[0])
                row = ticker_df.loc[ticker_df['Date'] == date].values[0].tolist()[1:]
                curr_date_df.loc[len(curr_date_df.index)] = row
                curr_date_df.to_csv(f"./data/dates/{date}.csv")
        except:
            bad_stocks.append(ticker)
    print(bad_stocks)


# input: list of dates, list of tickers, list of columns.
# output: none.
# the main function that unionize all the functions in order that needs to be ran in this part of the code.
def dates_edit_main(tickers, dates, columns):
    t1 = time.perf_counter()
    df_sp = pd.read_csv(SNPPATH)
    df_sp = df_sp.iloc[:-100, :]
    columns.remove('Date')
    creating_dates(dates, columns)
    stocks_to_dates(tickers, dates)
    get_advance_decline_ratio(dates, df_sp)
    calc_mcclellan(dates)

    t2 = time.perf_counter()
    print(f'Finished dates_edit_main in {t2 - t1} seconds')
