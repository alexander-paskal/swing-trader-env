"""
Visualizes trades on a single stock. Requires plotly to be installed
"""
# standard lib imports
from typing import List
from datetime import datetime

# local imports
from swing_trader_env.types import BuyAction, SellAction, BuyEvent, SellEvent
from swing_trader_env.core.utils import Date

# external dependenies
import pandas as pd
import plotly
import plotly.graph_objects as go


def viz_single_stock(
    df: pd.DataFrame,
    actions: List[BuyAction|SellAction],
    events: List[BuyEvent|SellEvent],
    start_date: datetime,
    end_date: datetime,
    
) -> plotly.graph_objects.Figure:
    """
    Visualization function for buy and sell actions performed on a single stock
    
    df: pd.DataFrame, yfinance-like dataframe containing the tick data
    actions: List[BuyAction|SellAction], the list of entered buy and sell actions
    events: List[BuyEvent|SellEvent], the list of filled buy and sell orders
    start_date: Date, the start date of the plot
    end_date: Date, the end date of the plot

    :returns plotly.graph_objects.Figure
    """

    # filter the dataframe
    df = df[df["Date"] >= start_date]
    df = df[df["Date"] <= end_date]

    # Create the action markers
    x_actions = []
    y_actions = []
    texts_actions = []
    colors_actions = []
    for action in actions:
        # action needs a date
        assert action.date_entered is not None, "cannot plot action without date_entered attribute filled. How are you calling this function? Make sure your actions all have this attribute filled in"
        
        x_actions.append(action.date_entered)
        price = df.loc[action.date_entered, "Close"]
        y_actions.append(price)
        
        action_type = "Buy" if isinstance(action, BuyAction) else "Sell" if isinstance(action, SellAction) else None
        color = "green" if isinstance(action, BuyAction) else "red" if isinstance(action, SellAction) else "gray"
        texts_actions.append(
            f"{action_type}, {action.shares} shares at ${round(price, 2)}"
        )
        colors_actions.append(color)


    # create the event markers
    x_events = []
    y_events = []
    texts_events = []
    colors_events = []
    for event in events:
        # event needs a date
        
        x_events.append(event.date_entered)
        price = df.loc[event.date_entered, "Open"]
        y_events.append(price)
        
        event_type = "Bought" if isinstance(event, BuyEvent) else "Bought" if isinstance(event, SellEvent) else None
        color = "green" if isinstance(event, BuyEvent) else "red" if isinstance(event, SellEvent) else "gray"
        texts_events.append(
            f"{event_type}, {event.shares} shares at ${round(price, 2)}"
        )
        colors_events.append(color)


    # Build the figure
    fig = go.Figure([
        # Add the underlying OHLC
        go.Ohlc(
            x=df['Date'],
            open=df['AAPL.Open'],
            high=df['AAPL.High'],
            low=df['AAPL.Low'],
            close=df['AAPL.Close'],
            increasing_line_color="black",
            decreasing_line_color="black",
            opacity=0.5,
        ),

        # Add the Action markers
        go.Scatter(
            x=x_actions, 
            y=y_actions, 
            #  mode="lines", 
            mode="markers+text",

            # marker settings
            marker_color=colors_actions,
            marker_size=15,
            opacity=0.5,

            # text settings
            text=texts_actions,
            textposition='top left',
        ),

        # Add the Event markers
        go.Scatter(
            x=x_events, 
            y=y_events, 
            #  mode="lines", 
            mode="markers+text",

            # marker settings
            marker_color=colors_events,
            marker_size=15,
            opacity=1,

            # text settings
            text=texts_events,
            textposition='top right',
        ),


    ])

    return fig



