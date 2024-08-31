"""
Simple script which builds a single stock environment and implements a simple agent
"""
# standard lib imports
# local imports
from swing_trader_env.env import SingleStockEnv
from swing_trader_env.types import BuyAction, SellAction
from swing_trader_env.core.utils import revenue
# external dependencies


def main():
    # instantiate the env
    env = SingleStockEnv(
        ticker="AAPL",
        start_date="2020-03-20",
        principal=10000,
        frequency="daily",
        data_path="swing-trader-old/data"
    )

    # step the environment 
    for i in range(100):

        # only make an action every 10th step
        if i % 10 != 0: 
            env.step()
            continue
        
        # buy on every on-20th action - Invest 90% of liquid capital
        if i % 20 == 0:
            buy_action = BuyAction(ticker="AAPL",shares= (0.9 * env.cash) / env.cur_price)
            env.step(buy_action)

        # sell on every off-20th action - Liquidate all shares held
        else:
            sell_action = SellAction(ticker="AAPL", shares=env.shares_held)
            env.step(sell_action)
    
    # print portfolio performance
    print(f"principal:       {env.principal}")
    print(f"portfolio value: {env.net_worth}")
    print(f"performance:     {env.performance}")

    # render the results
    env.render()

main()