# standard lib
from typing import List
from datetime import datetime

# local imports
from swing_trader_env.env.base import BaseEnv
from swing_trader_env.types import BuyAction, SellAction, BuyEvent, SellEvent
from swing_trader_env.core.utils import Date
from swing_trader_env.core.data import DataModel


class SingleStockEnv(BaseEnv):
    """
    Implements a single stock environment, which manages buys and sells of a single stock.
    """

    # public attributes
    ticker: str  # the stock ticker being traded
    cur_date: Date  # the current date of the simulation
    cur_price: float  # the most recent closing price of the stock
    start_date: Date  # the date that the simulation starts
    frequency: str  # the frequency being traded [daily, weekly, monthly]
    cash: float  # the amount of cash
    shares_held: float  # the number of shares held. Allows fractional 
    net_worth: float  # your current net worth, including liquid funds and assets
    principal: float  # the starting value of the portfolio

    # private attributes
    _data: DataModel  # the core data model modeling the stock
    _actions: List[BuyAction|SellAction]  # buy and sell actions
    _events: List[BuyEvent|SellEvent]  # buy and sell events


    def __init__(
            self,
            ticker: str,
            start_date: str|datetime|Date,
            principal: float,
            frequency: str = "daily",
    ):
        """
        Constructs a single-stock trading environment
        
        ticker: str, the ticker to trade
        start_date: Date, the date that the simulation starts
        principal: float, the starting cash amount
        frequency: str, the trading frequency. One of [daily, weekly, monthly]
        """
        # set identifying attributes
        self.set_ticker(ticker)
        self.set_start_date(start_date)
        self.set_principal(principal)
        self.set_frequency(frequency)

        # load data model
        self._data = DataModel(
            ticker=ticker,
            freqs=[frequency]
        )
        # reset stateful attributes
        self.reset()


    def set_principal(self, principal: float) -> None:
        """
        Sets the principal amount when beginning the scenario
        """
        assert principal > 0, "principal must be non-negative"
        self.principal = principal


    def set_frequency(self, frequency: str) -> None:
        """
        Sets the time frequency at which the environment steps
        """
        assert frequency in {"daily", "weekly", "monthly"}, "frequency must be one of 'daily','weekly','monthly'"
        self.frequency = frequency


    def set_ticker(self, ticker: str) -> None:
        """
        Sets the stock that environment is stepping
        """
        # TODO make sure the ticker is valid
        self.ticker = ticker
    

    def set_start_date(self, date: str|datetime|Date) -> None:
        """
        Set the start date of the simulation
        """
        date = Date(date)

        # TODO make sure that data exists for the stock simulation
        self.start_date = date
    

    def reset(self):
        """
        Reset the simulation
        """
        # reset public attributes
        self.cur_date = self.start_date
        self.cash = self.net_worth = self.principal
        self.shares_held = 0

        # reset private attributes
        self._events = []
        self._actions = []
    

    def step(self, action: BuyAction|SellAction|None = None) -> None:
        """
        Steps the environment one tick forward.

        Stepping runs through one day of trading, from pre-trading hours to open to close.
        only off-hours trading is allowed for now (day-trading support will come one day). Executes the following steps:

        1. Pretrading hours - accept BuyAction or SellAction market order as argument (must be one or the other). 
            Simulates entering an order in the evening after the market has closed
        2. Open - Jump to the open of the next trading day and fill any orders at the open price and generate corresponding BuyEvent or SellEvent
        3. Close - Jump to the close of the day and compute portfolio performance


        action: Optional, BuyAction or SellAction denoting the ticker to sell and the number of shares
        """
        
        # record buy or sell action and annotate date
        if isinstance(action, (BuyAction, SellAction)):
            action.date_entered = self.cur_date
            self._actions.append(action)

        # step the date forward
        self.cur_date = self._data.get_next_tick(self)
        open_price = self._data.get_price_on_open(self.cur_date)

        # Fill the orders at the open price of the current date, update holdings, and generate BuyEvent or Sellevent
        if isinstance(action, BuyAction):

            # verify sufficient funds
            assert self.cash >= open_price * action.shares, "Unable to place buy order - insufficient funds"

            # augment shares held
            self.shares_held += action.shares

            # subtract from cash
            self.cash -= open_price * action.shares

            # generate BuyEvent
            self._events.append(BuyEvent(
                ticker=self.ticker,
                shares=action.shares,
                price=open_price,
                date=self.cur_date,
            ))

        elif isinstance(action, SellAction):
            
            # verify sufficient shares held - no short selling allowed (one day i'll add it in)
            assert self.shares_held >= action.shares, "Unable to place sell order - insufficient shares held. Short selling is not permitted"

            # decrease shares held
            self.shares_held -= action.shares

            # add to cash
            self.cash += open_price * action.shares

            # generate SellEvent
            self._events.append(SellEvent(
                ticker=self.ticker,
                shares=action.shares,
                price=open_price,
                date=self.cur_date,
            ))        

            
        # fast forward to end of day
        close_price = self._data.get_price_on_close(self.cur_date)

        # compute current portfolio value and performance based off close price
        self.net_worth = self.shares_held * close_price + self.cash
        self.performance = self.net_worth / self.principal
        self.cur_price = close_price

        return 


    def render(self, mode: str = "plotly"):
        """
        Renders the environment

        mode: str, the type of rendering to perform
        """

        if mode == "plotly":
            try:
                from swing_trader_env.core.viz.plotly_ import viz_single_stock
            except ImportError:
                raise ImportError("Cannot use plotly visualization backend - plotly has not been installed")

            fig = viz_single_stock(
                df=getattr(self._data, self.frequency),
                actions=self._actions,
                events=self._events,
                start_date=self.start_date.as_datetime,
                end_date=self.cur_date.as_datetime,
            )

            fig.show()

        elif mode == "matplotlib":
            raise NotImplementedError("There will come a day when we support this feature. BUT IT IS NOT THIS DAY!!")
        
        else:
            raise ValueError("Unrecognized render mode")
