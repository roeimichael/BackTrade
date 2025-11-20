import pandas as pd
import time
import pandas_ta as ta

from config.data_config import DataConfig
from config.path_config import PathConfig


def get_advance_decline_ratio(dates, df_sp):
    print("Calculating advance decline ratio...")
    adr, add = [], []

    for date in dates:
        date_file = PathConfig.DATA_DATES2_DIR / f"{date}.csv"
        date_df = pd.read_csv(date_file)

        advance = (date_df['PriceUp'] == 1).sum()
        decline = (date_df['PriceUp'] == -1).sum()

        if decline == 0:
            decline = 1e-12

        ad_ratio = advance / decline
        ad_difference = advance - decline

        date_df['AD_difference'] = ad_difference
        date_df['AD_RATIO'] = ad_ratio
        date_df.to_csv(date_file)

        add.append(ad_difference)
        adr.append(ad_ratio)

    df_sp['AD_difference'] = add
    df_sp['AD_ratio'] = adr
    df_sp.to_csv(PathConfig.SP500_FILE)


def calc_mcclellan(dates):
    print("Calculating McClellan indicator...")
    df = pd.read_csv(PathConfig.SP500_FILE, index_col=[0])
    add = df['AD_difference']

    ema19 = ta.ema((add * 0.1), 19)
    ema39 = ta.ema((add * 0.05), 39)
    mcclellanosc = ema19 - ema39

    df['mcclellanOSC'] = mcclellanosc
    mcclellansum = mcclellanosc.cumsum()
    df['mcclellanSUM'] = mcclellansum
    df.to_csv(PathConfig.SP500_FILE)

    for index, date in enumerate(dates):
        date_file = PathConfig.DATA_DATES2_DIR / f"{date}.csv"
        curr_df = pd.read_csv(date_file)

        df = df.reindex(columns=[col for col in df.columns if col != 'Target'] + ['Target'])

        if index >= 38:
            curr_df['mcclellanSUM'] = mcclellansum[index]
            curr_df['mcclellanOSC'] = mcclellanosc[index]

        curr_df.to_csv(date_file)


def get_high_corr(ticker, tickers):
    req_df = pd.read_csv(PathConfig.DATA_STOCKS_DIR / f"{ticker}.csv")
    req_close = req_df['Close']
    corr = []
    tickers_copy = [t for t in tickers if t != ticker]

    for stock in tickers_copy:
        test_df = pd.read_csv(PathConfig.DATA_STOCKS_DIR / f"{stock}.csv")
        test_close = test_df['Close']
        corr.append(test_close.corr(req_close))

    top3 = sorted(zip(corr, tickers_copy), reverse=True)[:3]
    return [x[1] for x in top3]


def creating_dates(dates, columns):
    print("Creating dates files...")
    for date in dates:
        df = pd.DataFrame(columns=columns)
        date_file = PathConfig.DATA_DATES2_DIR / f"{date}.csv"
        df.to_csv(date_file)


def stocks_to_dates(tickers, dates):
    print("Moving from stocks to dates files...")
    bad_stocks = []

    for index, ticker in enumerate(tickers):
        try:
            print(f"Currently at {index + 1} stock {ticker} out of {len(tickers)}")
            ticker_file = PathConfig.DATA_STOCKS_DIR / f"{ticker}.csv"
            ticker_df = pd.read_csv(ticker_file)

            for date in dates:
                date_file = PathConfig.DATA_DATES2_DIR / f"{date}.csv"
                curr_date_df = pd.read_csv(date_file, index_col=[0])

                row = ticker_df.loc[ticker_df['Date'] == date].values[0].tolist()[2:]
                curr_date_df.loc[len(curr_date_df.index)] = row
                curr_date_df.to_csv(date_file)

        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            bad_stocks.append(ticker)

    if bad_stocks:
        print(f"Bad stocks: {bad_stocks}")


def dates_edit_main(tickers, dates, columns):
    t1 = time.perf_counter()

    df_sp = pd.read_csv(PathConfig.SP500_FILE)
    df_sp = df_sp.iloc[:-100, :]

    creating_dates(dates, columns)
    stocks_to_dates(tickers, dates)
    get_advance_decline_ratio(dates, df_sp)
    calc_mcclellan(dates)

    t2 = time.perf_counter()
    print(f'Finished dates_edit_main in {t2 - t1:.2f} seconds')
