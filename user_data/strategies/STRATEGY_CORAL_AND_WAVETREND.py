# pragma pylint: disable=missing-docstring, invalid-name, pointless-string-statement

# --- Do not remove these libs ---
import numpy as np  # noqa
import pandas as pd  # noqa
from pandas import DataFrame

from freqtrade.strategy.interface import IStrategy

# --------------------------------
# Add your lib to import here
import talib.abstract as ta
import freqtrade.vendor.qtpylib.indicators as qtpylib


class STRATEGY_CORAL_AND_WAVETREND(IStrategy):
    """
    Strategy CORAL_AND_WAVETREND
    author@: Fractate_Dev
    github@: https://github.com/Fractate/freqbot
    How to use it?
    > python3 ./freqtrade/main.py -s CORAL_AND_WAVETREND
    """
    # Strategy interface version - allow new iterations of the strategy interface.
    # Check the documentation or the Sample strategy to get the latest version.
    INTERFACE_VERSION = 2

    # Minimal ROI designed for the strategy.
    # This attribute will be overridden if the config file contains "minimal_roi".
    minimal_roi = {
        "60": 0.01,
        "30": 0.02,
        "0": 0.04
    }

    # Optimal stoploss designed for the strategy.
    # This attribute will be overridden if the config file contains "stoploss".
    stoploss = -0.10

    # Trailing stoploss
    trailing_stop = False

    # Optimal timeframe for the strategy.
    timeframe = '5m'

    # Run "populate_indicators()" only for new candle.
    process_only_new_candles = False

    # These values can be overridden in the "ask_strategy" section in the config.
    use_sell_signal = True
    sell_profit_only = False
    ignore_roi_if_buy_signal = False

    # Number of candles the strategy requires before producing valid signals
    startup_candle_count: int = 20

    # Optional order type mapping.
    order_types = {
        'buy': 'limit',
        'sell': 'limit',
        'stoploss': 'market',
        'stoploss_on_exchange': False
    }

    # Optional order time in force.
    order_time_in_force = {
        'buy': 'gtc',
        'sell': 'gtc'
    }

    plot_config = {
        # Main plot indicators (Moving averages, ...)
        'main_plot': {
            'ema10': {'color': 'red'},
            'ema100': {'color': 'green'},
            'ema1000': {'color': 'blue'},
            'coral_trend':{'color':'black'},
        },
        'subplots': {
            # Subplots - each dict defines one additional plot
            "MACD": {
                'macd': {'color': 'blue'},
                'macdsignal': {'color': 'orange'},
            },
            "RSI": {
                'rsi': {'color': 'red'},
            }
        }
    }
    def informative_pairs(self):
        """
        Define additional, informative pair/interval combinations to be cached from the exchange.
        These pair/interval combinations are non-tradeable, unless they are part
        of the whitelist as well.
        For more information, please consult the documentation
        :return: List of tuples in the format (pair, interval)
            Sample: return [("ETH/USDT", "5m"),
                            ("BTC/USDT", "15m"),
                            ]
        """
        return []

    def coral_trend_calc(self, dataframe: DataFrame) -> DataFrame:
        # dataframe['adx'] = ta.ADX(dataframe)

        sm = 500
        cd = 0.4
        ebc=False
        ribm=False
        di = (sm - 1.0) / 2.0 + 1.0
        c1 = 2 / (di + 1.0)
        c2 = 1 - c1
        c3 = 3.0 * (cd * cd + cd * cd * cd)
        c4 = -3.0 * (2.0 * cd * cd + cd + cd * cd * cd)
        c5 = 3.0 * cd + 1.0 + cd * cd * cd + 3.0 * cd * cd
        i1 = c1*dataframe["close"] + c2*DataFrame.fillna(i1[1])
        i2 = c1*i1 + c2*DataFrame.fillna(i2[1])
        i3 = c1*i2 + c2*DataFrame.fillna(i3[1])
        i4 = c1*i3 + c2*DataFrame.fillna(i4[1])
        i5 = c1*i4 + c2*DataFrame.fillna(i5[1])
        i6 = c1*i5 + c2*DataFrame.fillna(i6[1])

        dataframe['coral_trend'] = -cd*cd*cd*i6 + c3*(i5) + c4*(i4) + c5*(i3)

        # // --------------------------------------------------------------------------
        # // For the Pinescript coders: Determining trend based on the mintick step.
        # // --------------------------------------------------------------------------
        # //bfrC = bfr - nz(bfr[1]) > syminfo.mintick ? green : bfr - nz(bfr[1]) < syminfo.mintick ? red : blue
        # bfrC = bfr > nz(bfr[1]) ? green : bfr < nz(bfr[1])  ? red : blue
        # tc=ebc?gray:bfrC
        # plot(ribm?na:bfr, title="Trend", linewidth=3, style=circles, color=tc)
        # bgcolor(ribm?bfrC:na, transp=50)
        # barcolor(ebc?bfrC:na)

    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Adds several different TA indicators to the given DataFrame

        Performance Note: For the best performance be frugal on the number of indicators
        you are using. Let uncomment only the indicator you are using in your strategies
        or your hyperopt configuration, otherwise you will waste your memory and CPU usage.
        :param dataframe: Dataframe with data from the exchange
        :param metadata: Additional information, like the currently traded pair
        :return: a Dataframe with all mandatory indicators for the strategies
        """

        # EMA - Exponential Moving Average
        dataframe['ema10'] = ta.EMA(dataframe, timeperiod=10)
        dataframe['ema100'] = ta.EMA(dataframe, timeperiod=100)
        dataframe['ema1000'] = ta.EMA(dataframe, timeperiod=1000)

        sm = 500
        cd = 0.4
        ebc=False
        ribm=False
        di = (sm - 1.0) / 2.0 + 1.0
        c1 = 2 / (di + 1.0)
        c2 = 1 - c1
        c3 = 3.0 * (cd * cd + cd * cd * cd)
        c4 = -3.0 * (2.0 * cd * cd + cd + cd * cd * cd)
        c5 = 3.0 * cd + 1.0 + cd * cd * cd + 3.0 * cd * cd
        dataframe['i1'] = c1*dataframe["close"] + c2*DataFrame.fillna(dataframe['i1'].shift(1))
        dataframe['i2'] = c1*dataframe['i1'] + c2*DataFrame.fillna(dataframe['i2'].shift(1))
        dataframe['i3'] = c1*dataframe['i2'] + c2*DataFrame.fillna(dataframe['i3'].shift(1))
        dataframe['i4'] = c1*dataframe['i3'] + c2*DataFrame.fillna(dataframe['i4'].shift(1))
        dataframe['i5'] = c1*dataframe['i4'] + c2*DataFrame.fillna(dataframe['i5'].shift(1))
        dataframe['i6'] = c1*dataframe['i5'] + c2*DataFrame.fillna(dataframe['i6'].shift(1))

        dataframe['coral_trend'] = -cd*cd*cd*dataframe['i6'] + c3*(dataframe['i5']) + c4*(dataframe['i4']) + c5*(dataframe['i3'])

        return dataframe

    def populate_buy_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the buy signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                # (qtpylib.crossed_above(dataframe['rsi'], 30)) &  # Signal: RSI crosses above 30
                # (dataframe['tema'] <= dataframe['bb_middleband']) &  # Guard: tema below BB middle
                # (dataframe['tema'] > dataframe['tema'].shift(1)) &  # Guard: tema is raising
                # (dataframe['volume'] > 0)  # Make sure Volume is not 0
                dataframe['ema10'].crossed_above(dataframe['ema100'])
            ),
            'buy'] = 1

        return dataframe

    def populate_sell_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        """
        Based on TA indicators, populates the sell signal for the given dataframe
        :param dataframe: DataFrame populated with indicators
        :param metadata: Additional information, like the currently traded pair
        :return: DataFrame with buy column
        """
        dataframe.loc[
            (
                # (qtpylib.crossed_above(dataframe['rsi'], 70)) &  # Signal: RSI crosses above 70
                # (dataframe['tema'] > dataframe['bb_middleband']) &  # Guard: tema above BB middle
                # (dataframe['tema'] < dataframe['tema'].shift(1)) &  # Guard: tema is falling
                # (dataframe['volume'] > 0)  # Make sure Volume is not 0
                dataframe['ema100'].crossed_above(dataframe['ema10'])
            ),
            'sell'] = 1
        return dataframe
