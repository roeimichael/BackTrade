from __future__ import (absolute_import, division, print_function, unicode_literals)

import sys
from pathlib import Path
import datetime
import pandas as pd
import time
from dateutil.relativedelta import relativedelta

sys.path.append(str(Path(__file__).parent.parent))

from config.trading_config import TradingConfig
from config.path_config import PathConfig
from config.data_config import DataConfig

from Strategies.run_strategy import Run_strategy
from Strategies.bollinger_three import Bollinger_three
from Strategies.ADX_strategy import adx_strat
from Strategies.alligator_strategy import Alligator_strategy
from Strategies.CMF_ATR_MACD_strategy import MACD_CMF_ATR_Strategy
from Strategies.TEMA_MACD_strategy import TEMA_MACD_strategy
from Strategies.temea20_tema60 import Tema20_tema60


def get_strategy_name(strategy_class):
    return str(strategy_class).split('.')[-1][:-2]


def load_tickers_from_file(file_path):
    tickers = []
    with open(file_path, "r") as f:
        ticker_list = f.read().split(",")
        for ticker in ticker_list:
            tickers.append(ticker.split(":")[1])
    return tickers


def get_strategy_names(strategies):
    return [get_strategy_name(strat) for strat in strategies]


def get_parameters():
    return {
        'cash': TradingConfig.CASH,
        'macd1': TradingConfig.MACD_FAST,
        'macd2': TradingConfig.MACD_SLOW,
        'macdsig': TradingConfig.MACD_SIGNAL,
        'atrperiod': TradingConfig.ATR_PERIOD,
        'atrdist': TradingConfig.ATR_DISTANCE,
        'order_pct': TradingConfig.ORDER_PERCENTAGE
    }


def run_backtest():
    t1 = time.perf_counter()

    strategies = [
        Bollinger_three,
        adx_strat,
        Alligator_strategy,
        MACD_CMF_ATR_Strategy,
        TEMA_MACD_strategy,
        Tema20_tema60
    ]

    tickers = load_tickers_from_file(PathConfig.GREEN_LIST_FILE)
    strategy_names = get_strategy_names(strategies)
    df = pd.DataFrame(index=tickers, columns=strategy_names)

    start_date = datetime.date.today() - relativedelta(years=TradingConfig.LOOKBACK_YEARS)
    interval = DataConfig.INTERVAL
    parameters = get_parameters()

    counter = 0
    total = len(tickers) * len(strategies)

    for ticker in tickers:
        for strategy in strategies:
            counter += 1
            print(f"Progress: {counter}/{total} - Testing {ticker} with {get_strategy_name(strategy)}")

            try:
                run_cerebro = Run_strategy(parameters, strategy)
                percentage = run_cerebro.runstrat(ticker, start_date, interval)
                df.loc[ticker][get_strategy_name(strategy)] = round(percentage, 3)

            except ZeroDivisionError:
                print(f"ZeroDivisionError: {ticker} - {get_strategy_name(strategy)}")
                df.loc[ticker][get_strategy_name(strategy)] = None

            except Exception as e:
                print(f"Error: {e}")
                print(f"Ticker: {ticker}, Strategy: {get_strategy_name(strategy)}")
                df.loc[ticker][get_strategy_name(strategy)] = None

    t2 = time.perf_counter()
    print(f'Finished in {t2 - t1:.2f} seconds')

    df.to_csv(PathConfig.RESULTS_FILE)
    print(f"Results saved to {PathConfig.RESULTS_FILE}")


if __name__ == '__main__':
    run_backtest()
