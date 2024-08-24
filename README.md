# swing-trader-env
A Gym-style environment for backtesting, live paper trading, and RL development built on top of yfinance, pandas and numpy. 

# Installation

TODO:
  - minimal requirements
TODO:
  - put on py_pi

# Core Data Model
At the core of swing trader environments is a DataModel built on top of Pandas. This manages interactions with yfinance, ticker frequencies, indicators, and anything else related to sanitizing the data. It can
be installed and used independently of the rest of the repo.

# Supported Environments
 
## SingleStockEnv

Implementing Buy and Sell actions on a single stock
- TODO Action Space
- TODO State Space
- TODO Reward Space
  
## PortfolioEnv
- TODO Action Space
- TODO State Space
- TODO Reward Space

## LivePortfolioEnv
A version of the PortfolioEnv that runs on live data. Supports serialization and refreshing data feeds on daily, weekly or monthly intervals

# Examples
TODO - SingleStockEnv + SimpleAgent
TODO - SingleStockEnv -> random rollouts from stock pool
TODO - 

#

