import pandas as pd
import time
from warnings import simplefilter

WINDOWSIZE = 10
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)


# concatenate the last Window_size dates following each date in the list so that the bot can recive updates information
# of the last 10 dates.
def concatnate_date(windowsize, dates):
    dates = dates[:658]
    print("concatnating the files...")
    reverseddates = dates[::-1]
    for i in range(len(reverseddates)):
        print(f"currently at {i} date :{reverseddates[i]} out of {len(reverseddates)}")
        df = pd.read_csv(f"./data/dates/{reverseddates[i]}.csv")
        for j in range(1, windowsize + 1):
            temp_df = pd.read_csv(f"./data/dates/{reverseddates[i + j]}.csv")
            columns = temp_df.columns.values.tolist()
            for col in columns:
                df[f"{col}-{j}"] = temp_df[col]
        df.to_csv(f"./data/dates/{reverseddates[i]}.csv")


# a side function created to remove columns that were accidently duplicated and needs to be removed.
def clear_unnamed(dates):
    print("removing unnamed columns...")
    for date in dates:
        df = pd.read_csv(f"./data/dates/{date}.csv")
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df.to_csv(f"./data/dates/{date}.csv")


# main function running the concatenation process
def concatanation_main(dates):
    t1 = time.perf_counter()
    concatnate_date(WINDOWSIZE, dates)
    clear_unnamed(dates)
    t2 = time.perf_counter()
    print(f'Finished concatanation_main in {t2 - t1} seconds')
