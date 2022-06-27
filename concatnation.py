import pandas as pd
import time
import otherfunctions as of
from warnings import simplefilter

WINDOWSIZE = 10
simplefilter(action="ignore", category=pd.errors.PerformanceWarning)



def concatnate_date(windowsize):
    reverseddates = dates.tolist()[::-1]
    for i in range(len(reverseddates)):
        print(f"currently at {i} date :{reverseddates[i]} out of {len(reverseddates)}")
        df = pd.read_csv(f"./data/dates/{reverseddates[i]}.csv")
        for j in range(1, windowsize + 1):
            temp_df = pd.read_csv(f"./data/dates/{reverseddates[i + j]}.csv")
            columns = temp_df.columns.values.tolist()
            for col in columns:
                df[f"{col}-{j}"] = temp_df[col]
        df.to_csv(f"./data/dates/{reverseddates[i]}.csv")


if __name__ == '__main__':
    t1 = time.perf_counter()
    tickers = of.get_tickers()
    dates = of.get_dates(tickers)
    concatnate_date(WINDOWSIZE)
    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
