# standard lib
from typing import List, Optional
from datetime import datetime

# local imports
from swing_trader_env.types import BuyEvent, SellEvent
from swing_trader_env.core.utils import Date

# external dependencies
import pandas as pd
import numpy as np


def revenue(
    df: pd.DataFrame,
    events: List[BuyEvent|SellEvent],
    start_date: datetime|pd.Timestamp|Date|str,
    end_date: datetime|pd.Timestamp|Date|str,
) -> np.ndarray:
    """
    Given a single stock dataframe, a start date and end date, and a list of events, 
    computes the revenue from the trades at each time t, where t has the same frequency as the dataframe

    df: pd.DataFrame, yfinance-like dataframe containing the tick data
    events: List[BuyEvent|SellEvent], the list of filled buy and sell orders
    start_date: Date, the start date of the plot
    end_date: Date, the end date of the plot
  
    """
    start_date = Date(start_date).as_datetime
    end_date = Date(end_date).as_datetime

    df = df[df["Date"] >= start_date]
    df = df[df["Date"] <= end_date]


    revenues = []
    last_revenue: float = 0  # the last revenue value
    last_buy: BuyEvent|None = None
    this_event: BuyEvent|SellEvent|None = None
    next_event: BuyEvent|SellEvent|None = events.pop(0)  # the next event to process
    for i, t in enumerate(df.index):

        if next_event is None or t < next_event.date:  # haven't reached the next event yet
            revenues.append(last_revenue)  # fill forward last revenue value
            continue
        
        # step events
        this_event = next_event
        next_event = events.pop(0) if len(events) > 0 else None


        # process event
        if isinstance(this_event, BuyEvent):  # don't do anything for buy events
            last_buy = this_event
            revenue = last_revenue
        
        elif isinstance(this_event, SellEvent):  # compute proceeds based on this sell price and last buy price
            proceeds = this_event.price - last_buy.price
            revenue = last_revenue + proceeds
            last_buy = None
        
        # step revenues
        revenues.append(revenue)
        last_revenue = revenue

        # reset this event to None
        this_event = None
    
    assert len(revenues) == len(df.index)

    return np.array(revenues)


                
    
        

            



        




