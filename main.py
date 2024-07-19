import time
import scanner
import datesEdit
import concatnation
import normalization
import yfinance as yf

# Constants
STOCKSCSV = "Stocks in the SP 500 Index.csv"
SP500TICKER = "^GSPC"
START = "2019-05-01"
END = "2022-05-01"
INTERVAL = '1d'


# Create S&P 500 DataFrame
def create_sp500():
    print("Creating S&P 500 tickers file...")
    stock = yf.Ticker(SP500TICKER)
    df_sp = stock.history(start=START, end=END, interval=INTERVAL)
    df_sp.drop(columns=['Dividends', 'Stock Splits'], inplace=True)
    df_sp.to_csv("S&P500.csv")
    return df_sp


# Read columns from a file
def read_columns(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]


# Main function
if __name__ == '__main__':
    t1 = time.perf_counter()

    # Get necessary data
    create_sp500()
    tickers = read_columns('./data/tickers.txt')
    dates = read_columns('./data/dates.txt')
    columns = read_columns('./data/columns_small.txt')

    # Run the processing steps
    scanner.main(tickers)
    normalization.normalization_main(tickers)
    dates = dates[:658]  # Remove the last 100 days because of normalization window
    datesEdit.dates_edit_main(tickers, dates, columns)
    concatnation.concatanation_main(dates)

    t2 = time.perf_counter()
    print(f'Finished main in {t2 - t1} seconds')
