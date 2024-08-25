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
TODO - Portfolio + SimpleAgent
  - Selection
  - Purchase
TODO - Portfolio + SimpleAgent with portfolio ratios
TODO - Portfolio + SimpleAgent and stop losses
TODO - Portfolio in GymEnv wrapper with vector action and obs space
TODO - Options for scanning stocks

# Other Stuff
TODO - Loading data in 3 levels potentially? Reading an SQLite file, reading a csv, and pulling from yfinance
  - option to preload tickers of certain frequency, timeframe and indicator values and save in a database
  - option to save computations that have been loaded to a sqlite file
  - option to clear existing saves
  - option to view the total memory that's been used for data
  - comparison of parsing a csv with known types vs parsing an sqlite file

