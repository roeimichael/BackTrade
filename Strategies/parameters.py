import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.trading_config import TradingConfig


class Parameters:
    cash = TradingConfig.CASH
    macd2 = TradingConfig.MACD_SLOW
    macdsig = TradingConfig.MACD_SIGNAL
    atrperiod = TradingConfig.ATR_PERIOD
    atrdist = TradingConfig.ATR_DISTANCE
    order_pct = TradingConfig.ORDER_PERCENTAGE
