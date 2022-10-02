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


# input: none.
# output: data frame containing all the tickers of the s&p with basic information.
# the function calls for YF to get the information about the S&p iteslf.
def create_Sp500():
    print("creating s&p 500 tickers file...")
    stock = yf.Ticker(SP500TICKER)
    df_sp = stock.history(start=START, end=END, interval=INTERVAL)
    df_sp = df_sp.drop(columns=['Dividends', 'Stock Splits'])
    df_sp.to_csv(f"S&P500.csv")
    return df_sp


# input: none.
# output: list of all columns that are used in the data.
# the function reads from a premade file all the columns and puts them in a list.
def get_columns():
    columns_names = []
    with open('./data/columns.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            columns_names.append(x)
    return columns_names


# input: none.
# output: list of all dates that are used to receive the data.
# get all dates in use (3 years between 01/05/2019 to 01/05/2022).
def get_dates():
    dates_list = []
    with open('./data/dates.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            dates_list.append(x)
    return dates_list


# input: none.
# output: list of all tickers in the S&P500 index.
# the function reads from a premade file all the tickers and puts them in a list.
def get_tickers():
    stocks_tickers = []
    with open('./data/tickers.txt', 'r') as fp:
        for line in fp:
            x = line[:-1]
            stocks_tickers.append(x)
    return stocks_tickers


# input: none.
# output: none.
# this is the main function of the project it runs every other operation to create the final data.
if __name__ == '__main__':
    # gets needed data
    create_Sp500()
    tickers = get_tickers()
    dates = get_dates()
    columns = get_columns()
    # runs the code part by part
    # scanner.main(tickers)
    # normalization.normalization_main(tickers)
    dates = dates[:658]  # removes 100 last days beacuse of normalization window
    datesEdit.dates_edit_main(tickers, dates, columns)
    concatnation.concatanation_main(dates)
