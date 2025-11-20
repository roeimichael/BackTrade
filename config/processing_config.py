class ProcessingConfig:
    SPLITS = 25
    TARGET_THRESHOLD = 0.02
    NORMALIZATION_WINDOW_SIZE = 100
    CONCATENATION_WINDOW_SIZE = 10

    NOT_NORMALIZED = [
        "ma200", "ma50", "TRIX", "stochK", "stochD", "TRANGE", "BBupperband", "BBmiddleband", "BBlowerband",
        "ao", "cci", "coppock", "mom", "pgo", "alma", "dema", "wma", "fwma", "hma", "hwma", "jma", "kama",
        "mcgd", "pwma", "sinwma", "swma", "tema", "trima", "t3", "vidya", "vwma", "zlma", "qstick", "vhf",
        "atr", "massi", "pdist", "rvi", "ui", "ad", "adosc", "cmf", "efi", "obv", "pvt", "Market Cap", "DPC",
        "Cumulative Return"
    ]

    NORMALIZED = [
        "ADX", "ADXR", "AROONOSC", "DX", "PPO", "ULTOSC", "MACD", "MACDSIG", "MACDHIS", "apo", "bias", "bop",
        "cfo", "cmo", "cti", "inertia", "psl", "roc", "rsi", "rsx", "willr", "chop", "increasing", "decreasing",
        "mfi", "pvr", "ebsw", "PriceUp", "PriceDown", "VIX", "VVIX", "VXN"
    ]

    NOT_NORMALIZED_SMALL = [
        "ma50", "ma200", "TRIX", "stochK", "stochD", "TRANGE", "BBupperband", "BBmiddleband", "BBlowerband",
        "cci", "mom", "wma", "tema", "atr", "rvi", "Market Cap", "DPC", "Cumulative Return"
    ]
