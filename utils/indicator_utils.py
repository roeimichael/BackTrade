import talib
import pandas as pd
from config.indicator_config import IndicatorConfig


def add_talib_indicators(df: pd.DataFrame, subset: bool = False) -> None:
    df['ma50'] = df['Open'].rolling(IndicatorConfig.MA_PERIOD_SHORT).mean()
    df['ma200'] = df['Open'].rolling(IndicatorConfig.MA_PERIOD_LONG).mean()
    df['ADX'] = talib.ADX(df['High'], df['Low'], df['Close'], timeperiod=IndicatorConfig.ADX_TIMEPERIOD)
    df['ADXR'] = talib.ADXR(df['High'], df['Low'], df['Close'], timeperiod=IndicatorConfig.ADXR_TIMEPERIOD)
    df['AROONOSC'] = talib.AROONOSC(df['High'], df['Low'], timeperiod=IndicatorConfig.AROONOSC_TIMEPERIOD)

    if not subset:
        df['DX'] = talib.DX(df['High'], df['Low'], df['Close'], timeperiod=IndicatorConfig.DX_TIMEPERIOD)
        df['PPO'] = talib.PPO(df['Close'], fastperiod=IndicatorConfig.PPO_FAST_PERIOD,
                              slowperiod=IndicatorConfig.PPO_SLOW_PERIOD)

    df['stochK'], df['stochD'] = talib.STOCH(
        df['High'], df['Low'], df['Close'],
        fastk_period=IndicatorConfig.STOCH_FASTK_PERIOD,
        slowk_period=IndicatorConfig.STOCH_SLOWK_PERIOD,
        slowk_matype=IndicatorConfig.STOCH_SLOWK_MATYPE,
        slowd_period=IndicatorConfig.STOCH_SLOWD_PERIOD,
        slowd_matype=IndicatorConfig.STOCH_SLOWD_MATYPE
    )

    df['TRIX'] = talib.TRIX(df['Close'], timeperiod=IndicatorConfig.TRIX_TIMEPERIOD)
    df['ULTOSC'] = talib.ULTOSC(
        df['High'], df['Low'], df['Close'],
        timeperiod1=IndicatorConfig.ULTOSC_TIMEPERIOD1,
        timeperiod2=IndicatorConfig.ULTOSC_TIMEPERIOD2,
        timeperiod3=IndicatorConfig.ULTOSC_TIMEPERIOD3
    )

    df['MACD'], df['MACDSIG'], df['MACDHIST'] = talib.MACD(
        df['Close'],
        fastperiod=IndicatorConfig.MACD_FAST_PERIOD,
        slowperiod=IndicatorConfig.MACD_SLOW_PERIOD,
        signalperiod=IndicatorConfig.MACD_SIGNAL_PERIOD
    )

    df['TRANGE'] = talib.TRANGE(df['High'], df['Low'], df['Close'])
    df['BBupperband'], df['BBmiddleband'], df['BBlowerband'] = talib.BBANDS(
        df['Close'],
        timeperiod=IndicatorConfig.BBANDS_TIMEPERIOD,
        nbdevup=IndicatorConfig.BBANDS_NBDEVUP,
        nbdevdn=IndicatorConfig.BBANDS_NBDEVDN,
        matype=IndicatorConfig.BBANDS_MATYPE
    )


def add_pandas_ta_indicators(df: pd.DataFrame, subset: bool = False) -> None:
    if subset:
        indicators = [
            ('apo', df.ta.apo()),
            ('cci', df.ta.cci()),
            ('cfo', df.ta.cfo()),
            ('cmo', df.ta.cmo()),
            ('cti', df.ta.cti()),
            ('mom', df.ta.mom()),
            ('roc', df.ta.roc()),
            ('rsi', df.ta.rsi()),
            ('rsx', df.ta.rsx()),
            ('willr', df.ta.willr()),
            ('wma', df.ta.wma()),
            ('tema', df.ta.tema()),
            ('atr', df.ta.atr()),
            ('rvi', df.ta.rvi())
        ]
    else:
        indicators = [
            ('ao', df.ta.ao()),
            ('apo', df.ta.apo()),
            ('bias', df.ta.bias()),
            ('bop', df.ta.bop()),
            ('cci', df.ta.cci()),
            ('cfo', df.ta.cfo()),
            ('cmo', df.ta.cmo()),
            ('coppock', df.ta.coppock()),
            ('cti', df.ta.cti()),
            ('inertia', df.ta.inertia()),
            ('mom', df.ta.mom()),
            ('pgo', df.ta.pgo()),
            ('psl', df.ta.psl()),
            ('roc', df.ta.roc()),
            ('rsi', df.ta.rsi()),
            ('rsx', df.ta.rsx()),
            ('willr', df.ta.willr()),
            ('alma', df.ta.alma()),
            ('dema', df.ta.dema()),
            ('wma', df.ta.wma()),
            ('fwma', df.ta.fwma()),
            ('hma', df.ta.hma()),
            ('hwma', df.ta.hwma()),
            ('jma', df.ta.jma()),
            ('kama', df.ta.kama()),
            ('pwma', df.ta.pwma()),
            ('sinwma', df.ta.sinwma()),
            ('swma', df.ta.swma()),
            ('t3', df.ta.t3()),
            ('tema', df.ta.tema()),
            ('trima', df.ta.trima()),
            ('vwma', df.ta.vwma()),
            ('zlma', df.ta.zlma()),
            ('chop', df.ta.chop()),
            ('increasing', df.ta.increasing()),
            ('decreasing', df.ta.decreasing()),
            ('qstick', df.ta.qstick()),
            ('vhf', df.ta.vhf()),
            ('atr', df.ta.atr()),
            ('massi', df.ta.massi()),
            ('pdist', df.ta.pdist()),
            ('rvi', df.ta.rvi()),
            ('ui', df.ta.ui()),
            ('ad', df.ta.ad()),
            ('adosc', df.ta.adosc()),
            ('cmf', df.ta.cmf()),
            ('efi', df.ta.efi()),
            ('mfi', df.ta.mfi()),
            ('obv', df.ta.obv()),
            ('pvr', df.ta.pvr()),
            ('pvt', df.ta.pvt()),
            ('ebsw', df.ta.ebsw())
        ]

    for name, indicator in indicators:
        try:
            df[name] = indicator
        except Exception as e:
            print(f"Problem with indicator: {name} - {e}")
