# standard lib
from typing import Union
from datetime import datetime

# local imports
from swing_trader_env.env.base import BaseEnv
from swing_trader_env.types import BuyAction, SellAction, BuyEvent, SellEvent
from swing_trader_env.core.utils import Date

class SingleStockEnv(BaseEnv):
    """
    Implements a single stock environment, which manages buys and sells of a single stock.
    """

    # public attributes
    ticker: str  # the stock ticker being traded
    start_date: Date  # the date that the simulation starts
    frequency: str  # the frequency being traded [daily, weekly, monthly]

    # private attributes
    _start_date: Date  # the start date of the simulation
    _cur_date: Date  # the current date of the simulation TODO ?
    _events: List[BuyEvent|SellEvent]  # buy and sell events
    

    def set_frequency(frequency: str) -> None:
        """Sets the time frequency at which the environment steps"""


    def set_ticker(ticker: str) -> None:
        """
        Sets the stock that environment is stepping
        """
        # TODO make sure the ticker is valid
        self.ticker = ticker
    

    def set_start_date(date: str|datetime|Date):
        """
        Set the start date of the simulation
        """
        date = Date(date)

        # TODO make sure that data exists for the stock simulation
        
        self.date = date
    

    def step(self, action: BuyAction|SellAction|None = None):
        """
        Steps the environment one tick forward

        action: Optional, BuyAction or SellAction denoting the ticker to sell and the number of shares
        """
    
        raise NotImplementedError

    def reset(self):
        """
        Resets the environment
        """

        # load the ticker data
        # filter by the correct date
        # reset the stock history

    def render(self, mode: str = "plotly"):
        """
        Renders the environment

        mode: str, the type of rendering to perform
        """

        if mode == "plotly":
            raise NotImplementedError
        
        elif mode == "matplotlib":
            raise NotImplementedError
        
        else:
            raise ValueError("Unrecognized render mode")
