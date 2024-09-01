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
    def _compute(self, df: pd.DataFrame) -> pd.Series:
        """
        computes the indicator value

        df: pd.DataFrame, yfinance like dataframe. Index is set to 'Date' column

        :returns pd.DataFrame, same dataframe with the added column 
        """
        raise NotImplementedError
    

    @abc.abstractmethod
    def _name(self) -> str:
        """
        computes the indicator name. Should follow the convention

        {class_name}-{arg1}_{arg2}_..._{arg3}

        example:
        
            sma-50
            macd-12_26_9
            macd_hist-12_26_9


        """
        raise NotImplementedError
    
    
    def __call__(self, df: pd.DataFrame, inplace: bool = True) -> pd.DataFrame:
        """
        Main function. Calls abstract method _compute of each indicator

        df: pd.DataFrame, yfinance like dataframe. Index is set to 'Date' column
        inplace: bool, whether or not to modify the dataframe inplace or make a copy

        :returns pd.DataFrame, same dataframe with the added column 
        """
        if not inplace:
            df = df.copy(deep=True)
        
        series = self._compute(df)

        df[self._name()] = series
        return df
    
    def plot(
        self,
        series: pd.Series,
        *,
        mode: str="matplotlib",
        ax: Any = None, # plt.axes.Axes, runtime import/type check,
        **kwargs
    ) -> Any:  
        """
        User-facing plot function. Dispatches to private methods based on the plot
        mode
        """
        
        if mode == "matplotlib":
            try:
                import matplotlib.pyplot as plt
            except ImportError:
                raise ImportError("cannot use render mode 'matplotlib' - matplotlib is not installed")

            return self._plot_matplotlib(series, ax=ax, **kwargs)

        elif mode == "plotly":

            try:
                import plotly
            except ImportError:
                raise ImportError("cannot use render mode 'plotly' - plotly is not installed")
            
            return self._plot_plotly(self, series, **kwargs)

        else:
            raise ValueError(f"unrecognized render mode: '{mode}'")
    

    def _plot_matplotlib(
        self,
        series: pd.Series,
        *,
        ax: Any = None, # Optional[plt.axes.Axes]
        **kwargs
    ) -> Any:  # plt.axes.Axes
        """
        Import matplotlib within this function. Implementation of matplotlib plotting
        """

        raise NotImplementedError
    
    
    def _plot_plotly(
        self,
        series: pd.Series,
        **kwargs
    ) -> Any:  # plt.axes.Axes
        """
        Import plotly within this function. Implementation of plotly plotting
        """

        raise NotImplementedError