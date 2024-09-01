"""
Ichimoku cloud indicators

"""
# local imports
from swing_trader_env.core.indicators.base import Indicator

# external imports
import pandas as pd



class tenkan_sen(Indicator):
    def __init__(self, period: int = 9):
        self.period = period
    
    def _compute(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Tenkan-sen (Conversion Line).

        Tenkan-sen is the average of the high and low prices over a short period (default 9 periods).
        """
        return (df['High'].rolling(window=self.period).max() + df['Low'].rolling(window=self.period).min()) / 2
    
    def _name(self) -> str:
        return f"tenkan_sen-{self.period}"


class kijun_sen(Indicator):
    def __init__(self, period: int = 26):
        self.period = period
    
    def _compute(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Kijun-sen (Base Line).

        Kijun-sen is the average of the high and low prices over a medium period (default 26 periods).
        """
        return (df['High'].rolling(window=self.period).max() + df['Low'].rolling(window=self.period).min()) / 2
    
    def _name(self) -> str:
        return f"kijun_sen-{self.period}"


class senkou_span_a(Indicator):
    def __init__(self, period1: int = 9, period2: int = 26):
        self.period1 = period1
        self.period2 = period2
    
    def _compute(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Senkou Span A (Leading Span A).

        Senkou Span A is the average of the Tenkan-sen and Kijun-sen, shifted 26 periods ahead.
        """
        tenkan_sen = (df['High'].rolling(window=self.period1).max() + df['Low'].rolling(window=self.period1).min()) / 2
        kijun_sen = (df['High'].rolling(window=self.period2).max() + df['Low'].rolling(window=self.period2).min()) / 2
        return ((tenkan_sen + kijun_sen) / 2).shift(26)
    
    def _name(self) -> str:
        return f"senkou_span_a-{self.period1}_{self.period2}"


class senkou_span_b(Indicator):
    def __init__(self, period: int = 52, shift: int = 26):
        self.period = period
        self.shift = shift
    
    def _compute(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Senkou Span B (Leading Span B).

        Senkou Span B is the average of the high and low prices over a long period (default 52 periods), shifted 26 periods ahead.
        """
        return ((df['High'].rolling(window=self.period).max() + df['Low'].rolling(window=self.period).min()) / 2).shift(self.shift)
    
    def _name(self) -> str:
        return f"senkou_span_b-{self.period}_{self.shift}"


class chikou_span(Indicator):
    def __init__(self, shift: int = 26):
        self.shift = shift
    
    def _compute(self, df: pd.DataFrame) -> pd.Series:
        """
        Computes the Chikou Span (Lagging Span).

        Chikou Span is the close price shifted back by a default period (26 periods).
        """
        return df['Close'].shift(-self.shift)
    
    def _name(self) -> str:
        return f"chikou_span-{self.shift}"
