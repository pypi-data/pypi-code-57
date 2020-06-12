from jamboree import Jamboree, DBHandler # This is how we connect to databases and outside systems
import pandas as pd
import uuid
import time
from jamboree.utils.core import consistent_hash
# Handlers are ways to manage events and everything related to events. 
# They abstract all of the push and pull operations

class OrderHandler(DBHandler):
    def __init__(self):
        # We totally need to call this. Don't forget to do it.
        super().__init__()
        # The code base checks for these fields prior to any insert operations
        # They're also used to generate a key. A key is like a lane where we append events in a sorted manner.
        # This is also useful when you need information for other parts of the system, such as to keep track of time.
        self.entity = "orders" # An entity is a name of a real world distinguishable object
        self.required = {
            "exchange": str,
            "broker": str,
            "user_id": str,
            "episode": str,
            "live": bool
        }
        self._is_event = False
        self.order_fields = ['status', 'price', 'amount']
        self.allowed_statuses = ["OPEN", "PARTIAL", "FILLED", "CANCELLED"]
        self.order_status_paths = {
            "OPEN": ["PARTIAL", "FILLED", "CANCELLED"],
            "PARTIAL": ["FILLED", "CANCELLED"]
        }
        self.transistionable = ["OPEN", "PARTIAL"]
    
    @property
    def history(self):
        """ Returns a list of all the last 500 orders with this specific profile in a dataframe """
        all_orders = self.many(ar="relative")
        if len(all_orders) == 0:
            return []
        order_frame = pd.DataFrame(all_orders)
        _to_datetime = pd.to_datetime(order_frame.time, unit='s')
        order_frame = order_frame.drop(columns=['mtype', 'user_id', "broker", "exchange", "live", "timestamp", "episode", "time"])
        order_frame.set_index(_to_datetime, inplace=True)
        return order_frame
    
    @property
    def open_orders_spec(self):
        """ Get all open orders by exchange, broker, user_id, episode, live """
        pass
    
    @property
    def closed_orders_spec(self):
        """ Get all open orders by exchange, broker, user_id, episode, live """
        pass
    
    @property
    def current_time(self):
        return time.time()

    def is_valid_order(self, _order:dict):
        return all(field in _order.keys() for field in self.order_fields)
    
    def check_order_status(self, status:str, prior:str):
        if prior in self.transistionable:
            allowed_transitions = self.order_status_paths[prior]
            if status in allowed_transitions:
                return True
        return False
    
    def save_order(self, price:float, amount:float, status:str, order_number:int, order_id:str=None):
        """ Saves order information """
        self['order_num'] = order_number
        # Get the last order with that order number
        if status not in self.allowed_statuses:
            return
        """
            `self.last()`
        """ 
        previous_order = self.last()
        if len(previous_order.keys()) == 0:
            if status != "OPEN":
                print("New orders must be 'OPEN'")
                return
            order = {}
            _total = price * amount
            order['price'] = price
            order['amount'] = amount
            order['status'] = status
            order['total'] = _total
            order['time'] = self.current_time
            self.save(order)
            return
        
        prior_stat = previous_order.get('status')
        valid_prior = self.check_order_status(status, prior_stat)
        if valid_prior:
            order = {}
            _total = price * amount
            order['price'] = price
            order['amount'] = amount
            order['status'] = status
            order['total'] = _total
            order['time'] = self.current_time
            self.save(order)
        else:
            print("Not valid prior status")