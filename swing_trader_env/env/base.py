
# local imports
from swing_trader_env.types import Action


class BaseEnv:
    """
    Abstract Base Class for a stock environment
    """


    def step(self, action: Action):
        """
        Steps the environment forward one step

        action: Action (see swing_trader_env.types) - subclass of Action type
        
        """
        raise NotImplementedError


    def reset(self):
        """
        Resets the environment
        """
    
        raise NotImplementedError
    
    def render(self):
        """
        Renders the environment
        """