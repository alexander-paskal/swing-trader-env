"""
Example showing how to compute simple indicators for a simple stock
"""
# local imports
from swing_trader_env.core.data import DataModel
from swing_trader_env.core.indicators import sma, ema, macd, macd_hist
from swing_trader_env.core.utils import Date
from swing_trader_env.core.viz.matplotlib_ import plot_ohlc

# external imports
import matplotlib.pyplot as plt


def main():

    # load stock data
    stock_data = DataModel("AAPL", freqs=["daily", "weekly"], data_path="../swing-trader-old/data")

    # add indicator
    sma(period=50)(stock_data.daily)  # inplace by default to avoid unncessary data copying
    stock_data_copy_with_ema = ema(period=40)(stock_data.weekly, inplace=False)  # turn off inplace to copy the dataframe
    sma(period=200)(stock_data.daily)
    macd(12, 26)(stock_data.daily)
    macd_hist(12, 26, 9)(stock_data.daily)

    # filter the df
    df = stock_data.daily
    df = df[df.index >= Date("2020-01-01").as_timestamp]
    df = df[df.index <= Date("2020-12-31").as_timestamp]

    # extract the series that have been generated
    series_sma50 = df["sma-50"]
    series_sma200 = df["sma-200"]
    series_macd = df["macd-12_26"]
    series_macd_hist = df["macd_hist-12_26_9"]

    # plot the indicators
    ## gen a new axes 
    ax: plt.axes.Axes = macd_hist(12, 26, 9).plot(series_macd_hist, mode="matplotlib")
    plt.sca(ax)
    plt.title("MACD & the 'vid")
    plt.show()
    plt.cla()
    plt.clf()

    ## overlay on an existing axes
    ax: plt.axes.Axes = plt.subplot()
    sma(50).plot(series_sma50, mode="matplotlib", ax=ax, c="blue", label="50d")  # will pass through kwargs to plot function
    sma(200).plot(series_sma200, mode="matplotlib", ax=ax, c="red", label="200d")
    plt.sca(ax)
    plt.title("SMAs")
    plt.legend()
    plt.show()

    ## plot several indicators and an ohlc bar
    fig, axs = plt.subplots(2, 1)
    axs = axs.flatten()

    plot_ohlc(df, axs[0])
    sma(50).plot(series_sma50, ax=axs[0], c="blue")
    sma(200).plot(series_sma200, ax=axs[0], c="purple")
    macd_hist(12, 26, 9).plot(series_macd_hist, ax=axs[1])
    plt.show()

main()