import concatnation
import scanner
import normalization
import datesEdit
import pandas as pd
import yfinance as yf

STOCKSCSV = "Stocks in the SP 500 Index.csv"
SP500TICKER = "^GSPC"
START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'


# creates the defulat s&p file where some information is taken
def create_Sp500():
    stock = yf.Ticker(SP500TICKER)
    df_sp = stock.history(start=START, end=END, interval=INTERVAL)
    df_sp = df_sp.drop(columns=['Dividends', 'Stock Splits'])
    df_sp.to_csv(f"S&P500.csv")
    return df_sp


# gets the list of all columns used in the project
def get_columns():
    columns_names = []
    with open('columns.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            columns_names.append(x)
    return columns_names


# get all dates in use (3 years between 01/05/2019 to 01/05/2022
def get_dates():
    dates_list = []
    with open('dates.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            dates_list.append(x)
    return dates_list


# get the list of all tickers in the S&P that we need to iterate through
def get_tickers():
    stocks_tickers = []
    with open('tickers.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            stocks_tickers.append(x)
    return stocks_tickers


# runs all the files one after the other to complete the data
if __name__ == '__main__':
    # gets needed data
    create_Sp500()
    tickers = get_tickers()
    dates = get_dates()
    columns = get_columns()

    # runs the code itslef
    scanner.main(tickers)
    normalization.normalization_main(tickers)
    datesEdit.dates_edit_main(tickers, dates, columns)
    concatnation.concatanation_main(dates)
