""" 
    Create a price handler. Used to do all price commands that run throughout the application.
    This price handler should use lists, as it will be faster to handle.
"""


import uuid
from uuid import uuid1
from jamboree import Jamboree, DBHandler
from jamboree.handlers.complex.backtestable import BacktestDBHandler
from typing import Dict, Any, List


# NOTE: I'm probably going to have to separate everything here from

class StateSpaceHandler(BacktestDBHandler):
    """ 
        # State Space Management
        
        Create a statespace for the RL agent.

        Use this handler to manage collecting and storing a state space for reinforcement learning's requirements.         
    """
    def __init__(self, limit=5):
        super().__init__()
        self.entity = "state_space"
        self.required = {
            "name": str,
            "episode": str,
            "live": bool
        }
        self._limit = limit
    

    """ 
        ---------------------------------------------------------------------------------
        ----------------------------------- Properties ----------------------------------
        ---------------------------------------------------------------------------------
    """

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, _limit):
        self._limit = _limit


    

    def reset(self):
        """ No idea what goes here. But it should reset something."""
        super().reset()

def main():
    jam = Jamboree()
    statespace_handler = StateSpaceHandler()
    statespace_handler['name'] = "main_space"
    statespace_handler['episode'] = uuid.uuid4().hex
    statespace_handler['live'] = False
    statespace_handler.processor = jam


if __name__ == "__main__":
    main()