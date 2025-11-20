import pandas as pd
import time
from warnings import simplefilter

from config.processing_config import ProcessingConfig
from config.path_config import PathConfig

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


def concatnate_date(dates):
    print("Concatenating the files...")
    reversed_dates = dates[::-1]

    for i in range(len(reversed_dates) - ProcessingConfig.CONCATENATION_WINDOW_SIZE):
        print(f"Currently at {i} date: {reversed_dates[i]} out of {len(reversed_dates)}")

        file_path = PathConfig.DATA_DATES2_DIR / f"{reversed_dates[i]}.csv"
        df = pd.read_csv(file_path)

        for j in range(1, ProcessingConfig.CONCATENATION_WINDOW_SIZE + 1):
            temp_file_path = PathConfig.DATA_DATES2_DIR / f"{reversed_dates[i + j]}.csv"
            temp_df = pd.read_csv(temp_file_path)
            columns = temp_df.columns.values.tolist()

            for col in columns:
                if col != "ticker" and "Unnamed" not in col:
                    df[f"{col}-{j}"] = temp_df[col]

        df.to_csv(file_path)


def clear_unnamed(dates):
    print("Removing unnamed columns...")
    for date in dates:
        file_path = PathConfig.DATA_DATES2_DIR / f"{date}.csv"
        df = pd.read_csv(file_path)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv(file_path)


def concatanation_main(dates):
    t1 = time.perf_counter()
    clear_unnamed(dates)
    concatnate_date(dates)
    clear_unnamed(dates)
    t2 = time.perf_counter()
    print(f'Finished concatanation_main in {t2 - t1:.2f} seconds')
