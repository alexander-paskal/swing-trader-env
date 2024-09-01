# external imports
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as patches
import pandas as pd
from matplotlib.ticker import MaxNLocator


def plot_ohlc(df: pd.DataFrame, ax=None):
    """
    Plots OHLC (Open, High, Low, Close) bars from a DataFrame with columns Date, Open, High, Low, and Close.
    
    Args:
        df (pd.DataFrame): DataFrame containing OHLC data with columns 'Date', 'Open', 'High', 'Low', 'Close'.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(12, 6))

    # Convert 'Date' to datetime if it is not already
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'])

    # Plot OHLC bars
    for i, row in df.iterrows():
        color = 'green' if row['Close'] >= row['Open'] else 'red'
        ax.add_patch(patches.Rectangle(
            (mdates.date2num(row['Date']) - 0.3, min(row['Open'], row['Close'])),
            width=0.6,
            height=abs(row['Close'] - row['Open']),
            color=color
        ))
        ax.plot([mdates.date2num(row['Date']), mdates.date2num(row['Date'])],
                [row['Low'], row['High']],
                color=color, linewidth=1.5)

    # Formatting the x-axis as dates
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_minor_locator(mdates.DayLocator())
    ax.xaxis.set_tick_params(rotation=45)

    # Set labels and title
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title('OHLC Chart')

    # Add grid and legend
    ax.grid(True)
    ax.legend(['OHLC'], loc='best')

    return ax
    # plt.tight_layout()
    # plt.show()