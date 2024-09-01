"""
Indicator Base Class Definition
"""
# standard lib imports
from typing import Any
import abc

# external imports
import pandas as pd


class Indicator(abc.ABC):
    """
    A Base class for computing an indicator. Takes a YFinance Style dataframe, computes a technical
    indicator based on the stock price, and inserts it into the dataframe

    To create an indicator, subclass this class and implement the following abstract methods:
    __init__
    _compute
    _plot_matplotlib
    _plot_plotly
    
    """
    @abc.abstractmethod
    def __init__(self, *args):
        """
        Constructor. Unique to each indicator. Each instance of your indicator is
        itself a callable, which takes in a pandas dataframe and receives a pandas dataframe

        Positional arguments only
        """
        raise NotImplementedError

    @abc.abstractmethod    
    def __call__(self, df: pd.DataFrame, inplace: bool = True) -> pd.Series:
        """
        Main function. 

        df: pd.DataFrame, yfinance like dataframe. Index is set to 'Date' column
        inplace: bool, whether or not to modify the dataframe inplace or make a copy

        :returns pd.Series, column containing the indicator 
        """
        raise NotImplementedError
    