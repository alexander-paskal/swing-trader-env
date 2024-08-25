"""
Simple script which builds a single stock environment and implements a simple agent
"""
# standard lib imports
# local imports
from swing_trader_env.env import SingleStockEnv
from swing_trader_env.types import BuyAction, SellAction
# external dependencies


def main():
    # instantiate the env
    env = SingleStockEnv()

    # specify a Ticker/Date
    env.set_ticker("AAPL")
    env.set_date("2020-03-20")
    env.set_frequency("daily")
    # step the environment 
    for i in range(100):

        # only make an action every 10th step
        if i % 10 != 0: 
            env.step()
            continue
        
        # buy on every on-20th action
        elif i % 20 == 0:
            buy_action = BuyAction(ticker="AAPL",shares=1)
            env.step(buy_action)

        # sell on every off-20th action
        else:
            sell_action = SellAction(ticker="AAPL", shares=1)
            env.step(sell_action)
        

    # render the results
    env.render()
    