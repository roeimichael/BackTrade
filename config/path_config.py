import os
from pathlib import Path

class PathConfig:
    PROJECT_ROOT = Path(__file__).parent.parent

    DATA_DIR = PROJECT_ROOT / "data"
    DATA_NEW_DIR = PROJECT_ROOT / "data_new"
    DATA_STOCKS_DIR = DATA_DIR / "stocks"
    DATA_NEW_STOCKS_DIR = DATA_NEW_DIR / "stocks"
    DATA_DATES_DIR = DATA_DIR / "dates"
    DATA_DATES2_DIR = DATA_DIR / "dates2"
    DATA_DATES2_5_DIR = DATA_DIR / "dates2.5"
    DATA_SNP_DIR = DATA_DIR / "S&Pdata"

    TICKERS_FILE = DATA_DIR / "tickers.txt"
    DATES_FILE = DATA_DIR / "dates.txt"
    COLUMNS_SMALL_FILE = DATA_DIR / "columns_small.txt"
    COLUMNS_FILE = DATA_DIR / "columns.csv"
    TARGET_FILE = DATA_DIR / "target.csv"

    SP500_FILE = "S&P500.csv"
    GREEN_LIST_FILE = "Green list (4).txt"
    RESULTS_FILE = "results.csv"

    @classmethod
    def ensure_directories(cls):
        for attr_name in dir(cls):
            attr = getattr(cls, attr_name)
            if isinstance(attr, Path) and attr_name.endswith('_DIR'):
                attr.mkdir(parents=True, exist_ok=True)
