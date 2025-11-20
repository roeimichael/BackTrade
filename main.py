import time
import yfinance as yf

from config.data_config import DataConfig
from config.path_config import PathConfig
from config.processing_config import ProcessingConfig
from utils.file_utils import read_lines_from_file

import scanner
import datesEdit
import concatnation
import normalization


def create_sp500():
    print("Creating S&P 500 data file...")
    stock = yf.Ticker(DataConfig.SP500_TICKER)
    df_sp = stock.history(
        start=DataConfig.START_DATE,
        end=DataConfig.END_DATE,
        interval=DataConfig.INTERVAL
    )
    df_sp.drop(columns=['Dividends', 'Stock Splits'], inplace=True)
    df_sp.to_csv(PathConfig.SP500_FILE)
    return df_sp


def load_input_data():
    tickers = read_lines_from_file(PathConfig.TICKERS_FILE)
    dates = read_lines_from_file(PathConfig.DATES_FILE)
    columns = read_lines_from_file(PathConfig.COLUMNS_SMALL_FILE)
    return tickers, dates, columns


def run_data_pipeline(tickers, dates, columns):
    scanner.main(tickers)
    normalization.normalization_main(tickers)

    adjusted_dates = dates[:658]
    datesEdit.dates_edit_main(tickers, adjusted_dates, columns)
    concatnation.concatanation_main(adjusted_dates)


def main():
    t1 = time.perf_counter()

    PathConfig.ensure_directories()
    create_sp500()
    tickers, dates, columns = load_input_data()
    run_data_pipeline(tickers, dates, columns)

    t2 = time.perf_counter()
    print(f'Finished main in {t2 - t1:.2f} seconds')


if __name__ == '__main__':
    main()
