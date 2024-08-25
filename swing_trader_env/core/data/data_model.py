"""
Data Model contains all the data needed for the environment
"""
# standard lib
from typing import *
from typing_extensions import Self
import os

# local
from swing_trader_env.core.utils import Date

# external
import pandas as pd
import numpy as np
from datetime import datetime


__all__ = ['DataModel', 'NoDataException']


class NoDataException(Exception):
    pass


class DataModel:
    """
    Core data access for ticker information for a single ticker. Wraps pandas dataframes of different tick frequencies
    """

    # TODO handle loading non-existent data from yfinance
    # TODO handle loading data from a database
    # TODO how to optimize caching data in databases
    # TODO how to handle caching computations for different indicators

    ticker: str
    daily: pd.DataFrame
    weekly: pd.DataFrame
    monthly: pd.DataFrame

    data_path = "data"  # from root  # TODO figure out a more elegant way to handle this

    _synthetic_data: Dict[str, pd.DataFrame] = None

    def __init__(self, ticker: os.PathLike, freqs: List[str]):

    
        self.ticker = ticker
        
        for f in freqs:
            df = pd.read_csv(self._csv_path(ticker, f))

            if df.empty:
                raise NoDataException(f"No data! {ticker} - {f}")
            df = self._clean(df)
            setattr(self, f, df)
    

    def _csv_path(self, ticker: str, freq: str) -> os.PathLike:
        return os.path.join(self.data_path, freq, f"{ticker}-{freq}.csv")

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Cleans the dataframe"""
        df = df[["Date", "Open", "High", "Low", "Close", "Volume"]]
        df = df.dropna()

        df = df[df["Open"] != 0]
        df = df[df["Close"] != 0]
        
        date_df = df["Date"].str.split(" ", expand=True)[0]
        df["Date_str"] = date_df
        df["Date"] = pd.to_datetime(date_df)
        df = df.set_index("Date")
        return df
    
    def access(self, freq: str, date: Date, attrs: Optional[List[str]] = None, length: Optional[int] = None) -> Tuple[Dict, List[Dict]]:
        """
        Access the latest tick(s) of the frequency data based on date
        """
        date = Date(date)
        df = getattr(self, freq)

        df = df[df.index <= date.as_timestamp]

        if attrs is None:
            attrs = df.columns

        df = df[attrs]

        if length is None:
            length = 1
        
        df = df.iloc[-length:, :]

        return df

    def get_price_on_open(self, date: Date) -> float:
        """
        Get the open price on the next tick following a given tick
        """
        
        df = self.access(
            freq="daily",
            attrs=["Open"],
            date=Date(date),
            length=1
        )
        return df.iloc[0, 0]

    def get_price_on_close(self, date: Date) -> float:
        """
        Get the price at the close
        """
        df = self.access(
            freq="daily",
            attrs=["Close"],
            date=date,
            length=1
        )
        return df.iloc[0, 0]

    def get_next_tick(self, freq: str, date: Date) -> Date:
        """
        Get the next date at a given frequenc
        y"""
        return self.get_n_ticks_after(freq, date, 1)
    
    def get_n_ticks_after(self, freq: str, date: Date, n: int) -> Date:
        """Get the date N ticks later"""
        df = getattr(self, freq)
        i1 = list(df.index).index(Date(date).as_timestamp)
        i2 = i1 + n
        ts2 = df.index[i2]
        return Date(ts2)
    
    def get_date_bounds(self, freq: Optional[str] = None) -> Tuple[Date, Date]:
        """Returns the earliest and latest date contained within all specified frequencies. """
        if freq is None:
            freqs = ['daily', 'weekly', 'monthly']
        else:
            freqs = [freq]

        maxs, mins = [], []
        for freq in freqs:
            if hasattr(self, freq):
                df = getattr(self, freq)
                
                if df.empty:
                    continue
                df_dates = [d for d in df.index]
                maxs.append(max(df_dates))
                mins.append(min(df_dates))
        
        return Date(max(mins)), Date(min(maxs))

    def set_date_bounds(self, start: Date, end: Date, freq: Optional[str] = None):
        """Sets the date bounds (inclusive). Option to specify frequency"""
        
        start = Date(start)
        end = Date(end)
        
        if freq is None:
            freqs = ['daily', 'weekly', 'monthly']
        else:
            freqs = [freq]
        
        for freq in freqs:
            if hasattr(self, freq):
                df = getattr(self, freq)
                
                if df.empty:
                    continue

                df = df[df.index >= start.as_timestamp]
                df = df[df.index <= end.as_timestamp]

                setattr(self, freq, df)
    
    def buy_and_hold(self, start: Date, end: Date) -> float:
        return self.get_price_on_close(end) / self.get_price_on_open(start)

    def end_date(self) -> Date:
        return self.get_date_bounds()[1]