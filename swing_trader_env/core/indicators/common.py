# local imports
from typing import Any
from swing_trader_env.core.indicators.base import Indicator

# external imports
import pandas as pd


"""
Here are implementations of common indicators. A note on the naming conventions:

The series that shows up in your dataframe when you compute an indicator is going to be named in the following
way:

    {class_name}-{arg1}_{arg2}_..._{arg3}

where the class name will be lower snake case, and the arguments are those for the class constructor.
Example

    sma(period=50) -> 'sma-50'
    macd(fast=12,slow=26) -> 'macd-12_26'
    macd_hist(fast=12, slow=26, signal=9) -> 'macd_hist-12_26_9'

one could thus reconstruct an indicator from its name by using the following functions:

    name = 'macd_hist-12_26_9'
    class_name, arg_string = name.split('-')
    
    import sys
    class_var = getattr(sys.modules[__name__], class_name)  # reference the class by its string as part of this module
    args = [float(arg) for arg in arg_string.split("_")]
    indicator = class_var(*args)

"""


class sma(Indicator):
    """
    Simple Moving Average Indicator
    """
    period: int

    def __init__(self, period: int):
        self.period = period
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Simple Moving Average

            sma_t = SUM(
                p_{t - (n-1)}, p_{t - (n-2)}, ..., p_{t - 1}, p_{t}
            ) / i

        p = price
        t = index
        n = period    
        
        """

        return df['Close'].rolling(window=self.period).mean()
    


class ema(Indicator):
    """
    Simple Moving Average Indicator
    """
    period: int

    def __init__(self, period: int):
        self.period = period
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Exponential Moving Average

            (1) ema_t = alpha * p_t + (1 - alpha) * ema_{t-1}
            (2) alpha = 2 / (n + 1)

        p = price
        t = index
        n = period    
        
        """
        return df['Close'].ewm(span=50, adjust=False).mean()


class macd(Indicator):
    fast: int
    slow: int


    def __init__(self, fast: int, slow: int):
        self.fast = fast
        self.slow = slow
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Moving Average Convergence - Divergence Indicator

        ema(fast) - ema(slow)

        """

        fast = df['Close'].ewm(span=12, adjust=False).mean()
        slow = df['Close'].ewm(span=26, adjust=False).mean()

        return fast - slow
        

class macd_hist(Indicator):

    fast: int
    slow: int
    signal: int

    def __init__(self, fast: int, slow: int, signal: int):
        self.fast = fast
        self.slow = slow
        self.signal = signal

    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Moving Average Convergence - Divergence HistogramIndicator

        (1) macd = ema(fast) - ema(slow)
        (2) macd_hist = macd - ema(signal)(macd)

        """

        fast = df['Close'].ewm(span=12, adjust=False).mean()
        slow = df['Close'].ewm(span=26, adjust=False).mean()
        macd = fast - slow
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd - signal


class bollinger_upper(Indicator):

    period: int
    k: int

    def __init__(self, period: int, k: int):
        self.period = period
        self.k = k
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Bollinger band upper bound

        bollinger = sma(n)(p) + k * std(n)(p)

        n = period
        p = price
        std = standard deviation
        
        """

        # Calculate the Middle Band (SMA)
        middle = df['Close'].rolling(window=self.period).mean()

        # Calculate the Standard Deviation
        std = df['Close'].rolling(window=self.period).std()

        # Calculate the Upper and Lower Bands
        return middle + self.k * std


class bollinger_lower(Indicator):

    period: int
    k: int

    def __init__(self, period: int, k: int):
        self.period = period
        self.k = k
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Bollinger band upper bound

        bollinger = sma(n)(p) + k * std(n)(p)

        n = period
        p = price
        std = standard deviation
        
        """

        # Calculate the Middle Band (SMA)
        middle = df['Close'].rolling(window=self.period).mean()

        # Calculate the Standard Deviation
        std = df['Close'].rolling(window=self.period).std()

        # Calculate the Upper and Lower Bands
        return middle - self.k * std


class rsi(Indicator):

    period: int
    def __init__(self, period: int):
        self.period = period
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Relative Strength Index

        (1) gains = p[p_t > p_{t-1}]
        (2) losses = p[p_t < p_{t-1}]
        """
        n = self.period

        # Calculate the difference in price from the previous step
        delta = df['Close'].diff()

        # Separate gains and losses
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate the rolling average of gains and losses
        avg_gain = gain.rolling(window=n, min_periods=n).mean()
        avg_loss = loss.rolling(window=n, min_periods=n).mean()

        # Calculate the Relative Strength (RS)
        rs = avg_gain / avg_loss

        # Calculate the RSI
        return 100 - (100 / (1 + rs))
    

class stochastic_oscillator(Indicator):
    def __init__(self, period: int):
        self.period = period
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Stochastic Oscillator.

        This indicator measures the relative position of the close price within the high-low range over a specified period.
        """
        low_min = df['Low'].rolling(window=self.period).min()
        high_max = df['High'].rolling(window=self.period).max()
        return 100 * (df['Close'] - low_min) / (high_max - low_min)
    

class atr(Indicator):
    def __init__(self, period: int):
        self.period = period
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Average True Range (ATR).

        ATR measures market volatility. It is calculated as the average of True Ranges over a specified period.
        True Range is the maximum of:
        - High - Low
        - High - Previous Close
        - Low - Previous Close
        """
        prev_close = df["Close"].shift(1)
        tr_df = pd.DataFrame()

        tr_df["range_high_low"] = df["High"] - df["Low"]
        tr_df["range_high_prev_close"] = df["High"] - prev_close
        tr_df["range_low_prev_close"] = df["Low"] - prev_close
        
        tr = tr_df.abs().max(axis=1)

        return tr.rolling(window=self.period).mean()
    


class obv(Indicator):
    def __init__(self):
        pass
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the On-Balance Volume (OBV).

        OBV adds volume on up days and subtracts volume on down days. It helps to confirm price trends.
        """
        return (df['Volume'] * df['Close'].diff().apply(lambda x: 1 if x > 0 else -1)).cumsum()


class vwap(Indicator):
    def __init__(self):
        pass
    
    def __call__(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Volume Weighted Average Price (VWAP).

        VWAP is calculated as the cumulative sum of (Price x Volume) divided by the cumulative sum of Volume.
        """
        return (df['Close'] * df['Volume']).cumsum() / df['Volume'].cumsum()


