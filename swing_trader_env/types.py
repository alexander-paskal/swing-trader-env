"""
Contains all type definitions for swing trader environments
"""
# standard lib
from typing import List, Dict, Set, Tuple, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime


### Action Space

class Action:
    """Action base class"""
    pass

@dataclass
class BuyAction:
    """Buy Action. Analogous to submitting a market buy order"""

    """Stock ticker"""
    ticker: str

    """Number of shares. Allows fractional shares"""
    shares: float

@dataclass
class SellAction:
    """Sell Action. Analogous to submitting a market sell order"""

    """Stock ticker"""
    ticker: str

    """Number of shares. Allows fractional shares"""
    shares: float

@dataclass
class MultiBuyAction:

    """A list of all buy actions"""
    buy_actions: List[BuyAction]

@dataclass
class MultiSellAction:

    """A list of all sell actions"""
    sell_actions: List[SellAction]


### Events
@dataclass
class SellEvent:
    """Sell event. Equivalent to filling a sell order"""

    ticker: str
    shares: float
    price: float
    date: datetime

    @property
    def value(self) -> float:
        return self.price * self.shares

@dataclass
class BuyEvent:
    """Buy event. Equivalent to filling a buy order"""
    
    ticker: str
    shares: float
    price: float
    date: datetime

    @property
    def value(self) -> float:
        return self.price * self.shares