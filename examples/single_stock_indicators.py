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
    df = stock_data.daily

    # add indicator
    df["sma-50"] = sma(period=50)(stock_data.daily)  # inplace by default to avoid unncessary data copying
    df["sma-200"] = sma(period=200)(stock_data.daily)
    df["macd-12_26"] = macd(12, 26)(stock_data.daily)
    df["macd_hist-12_26_9"] = macd_hist(12, 26, 9)(stock_data.daily)

    # filter the df
    df = df[df.index >= Date("2020-01-01").as_timestamp]
    df = df[df.index <= Date("2020-12-31").as_timestamp]

    ## plot several indicators and an ohlc chart
    fig, axs = plt.subplots(2, 1)
    axs = axs.flatten()

    plot_ohlc(df, axs[0])
    axs[0].plot(df["sma-50"], c="blue", label="sma-50")
    axs[0].plot(df["sma-200"], c="purple", label="sma-200")
    
    pos = df["macd_hist-12_26_9"].where(df["macd_hist-12_26_9"] > 0, 0)
    neg = df["macd_hist-12_26_9"].where(df["macd_hist-12_26_9"] <= 0, 0)
    axs[1].bar(df.index, pos, color="green")
    axs[1].bar(df.index, neg, color="red")
    plt.show()

main()