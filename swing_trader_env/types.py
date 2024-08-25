"""
Contains all type definitions for swing trader environments
"""
# standard lib
from typing import List, Dict, Set, Tuple, Optional, Any, Union
from dataclasses import dataclass
from datetime import datetime


### Action Space

@ dataclass
class Action:
    """Action base class - functions as a market order"""

    """Stock ticker"""
    ticker: str

    """Number of shares. Allows fractional shares"""
    shares: float

    """Optional - date the order was entered. May be set externally"""
    date_entered: datetime|None = None

@dataclass
class BuyAction(Action):
    """Buy Action. Analogous to submitting a market buy order"""


@dataclass
class SellAction(Action):
    """Sell Action. Analogous to submitting a market sell order"""


@dataclass
class MultiAction:
    """
    A container class for multiple Buy or Sell actions
    """
    actions: List[BuyAction|SellAction]

    @property
    def buy_actions(self) -> List[BuyAction]:
        return [action for action in self.actions if isinstance(action, BuyAction)]

    @property
    def sell_actions(self) -> List[SellAction]:
        return [action for action in self.actions if isinstance(action, SellAction)]


### Events
@dataclass
class OrderFilledEvent:
    """
    Base class representing the event of an order being filled
    """
    ticker: str
    shares: float
    price: float
    date: datetime

    @property
    def value(self) -> float:
        return self.price * self.shares

@dataclass
class SellEvent(OrderFilledEvent):
    """Sell event. Equivalent to filling a sell order"""


@dataclass
class BuyEvent(OrderFilledEvent):
    """Buy event. Equivalent to filling a buy order"""
    