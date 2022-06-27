from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from Strategies.run_strategy import Run_strategy
from dateutil.relativedelta import relativedelta
from Strategies.bollinger_three import Bollinger_three
from Strategies.ADX_strategy import adx_strat
from Strategies.alligator_strategy import Alligator_strategy
from Strategies.CMF_ATR_MACD_strategy import MACD_CMF_ATR_Strategy
from Strategies.TEMA_MACD_strategy import TEMA_MACD_strategy
from Strategies.temea20_tema60 import Tema20_tema60
import datetime
import pandas as pd
import time


def get_strategy_name(start):
    return str(start).split('.')[-1][:-2]


def get_df_tickers():
    tickers = []
    f = open("Green list (4).txt", "r")
    list = f.read().split(",")
    for ticker in list:
        tickers.append(ticker.split(":")[1])
    return tickers


def get_df_strategies(strats):
   cols = []
   for strat in strats:
        cols.append(get_strategy_name(strat))
   return cols


if __name__ == '__main__':
    t1 = time.perf_counter()

    strategies = [Bollinger_three, adx_strat, Alligator_strategy, MACD_CMF_ATR_Strategy, TEMA_MACD_strategy, Tema20_tema60]
    tickers = get_df_tickers()
    strategy_list = get_df_strategies(strategies)
    df = pd.DataFrame(index=tickers, columns=strategy_list)
    start_date = datetime.date.today() - relativedelta(years=3)
    # end_date = "2021-09-23"
    # intervals = {"30m": "2021-09-01", "1h": "2021-08-25", "90m": "2021-08-01", "1d": "2021-06-01"}
    interval = "1d"
    parameters = dict(cash=10000,
                      macd1=12,
                      macd2=26,
                      macdsig=9,
                      atrperiod=14,
                      atrdist=2.0,
                      order_pct=1.0, )
    counter = 0
    for ticker in tickers:
        for strategy in strategies:
            counter += 1
            print(counter)
            try:
                run_cerebro = Run_strategy(parameters, strategy)
                percentage = run_cerebro.runstrat(ticker, start_date, interval)
                df.loc[ticker][get_strategy_name(strategy)] = round(percentage, 3)
            except ZeroDivisionError:
                print(ticker)
                print(get_strategy_name(strategy))
                df.loc[ticker][get_strategy_name(strategy)] = None
            except Exception as e:
                print(e)
                print(ticker)
                print(get_strategy_name(strategy))

    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1} seconds')
    df.to_csv('results.csv')
