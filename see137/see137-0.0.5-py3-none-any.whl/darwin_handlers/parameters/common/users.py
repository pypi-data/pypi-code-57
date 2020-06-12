from see137.parameters import Parameter
from jamboree.utils.core import consistent_hash

class UserParameter(Parameter):
    """ UserConfig """
    def __init__(self, userid:str, is_websocket=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = userid
        self.is_websocket = is_websocket
        
        # We're eventually allowing to point to another portfolio to begin the backtest on (start amount, allocation, etc) 
    