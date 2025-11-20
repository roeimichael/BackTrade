import time
import pandas as pd

from config.processing_config import ProcessingConfig
from config.path_config import PathConfig
from utils.normalization_utils import windownorm_normalization


def normalize_tickers(tickers):
    print("Normalizing all stock dataframes...")
    unavailable = []

    for index, ticker in enumerate(tickers):
        try:
            print(f"Currently processing {index + 1} of {len(tickers)}: {ticker}")
            file_path = PathConfig.DATA_STOCKS_DIR / f"{ticker}.csv"
            df = pd.read_csv(file_path)

            for column in ProcessingConfig.NOT_NORMALIZED_SMALL:
                if column in df.columns:
                    unnormalized_data = df[column].tolist()
                    normalized_data = windownorm_normalization(
                        unnormalized_data,
                        ProcessingConfig.NORMALIZATION_WINDOW_SIZE
                    )
                    df[column] = normalized_data

            df = df.iloc[:-ProcessingConfig.NORMALIZATION_WINDOW_SIZE, :]
            df.to_csv(file_path, index=False)

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
