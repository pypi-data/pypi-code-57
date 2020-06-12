import copy
import random
import uuid

import maya
from typing import Union, Optional
from addict import Dict as ADict
from jamboree import Jamboree
from jamboree.handlers.abstracted.search import ParameterizedSearch



def order_schema():
    schema = ADict()
    # exchange we're trading on
    schema.exchange = str
    # the pair we're trading on (symbol)
    schema.symbol = str
    # the amount of the base currency we're trading on
    schema.amount = float
    # the episode we're trading on. We can use to get
    schema.episode = str
    # The user the trade is started on
    schema.userid = str
    # Determines if this a live trade
    schema.live = bool
    # The side the trade is on
    schema.side = str
    # The order status (OPEN, CLOSED)
    schema.status = str
    # The time the trade initialized
    schema.timestamp = float

    # the price we initialize the trade at
    schema.init_price = float

    # The price we finished the price at
    schema.fill_price = float
    return schema.to_dict()


# PENDING = 'pending'
# OPEN = 'open'
# CANCELLED = 'cancelled'
# PARTIALLY_FILLED = 'partially_filled'
# FILLED = 'filled'


class OrderSearch(ParameterizedSearch):
    def __init__(self):
        super().__init__()
        self.entity = "order_search"
        self.dreq = order_schema()

        self.default = {"live": False, "status": "OPEN"}
        self.must_have = [
            'episode', 'userid', 'symbol', 'side', 'timestamp', 'exchange',
            'amount', 'init_price'
        ]
        self.allowed_statuses = ["PENDING", "OPEN", "CANCELLED", "PARTIAL", "FILLED"]

    def init(self, **kwargs):
        """ Starts a new order. Doesn't allow for"""
        _default = copy.copy(self.default)
        _default.update(kwargs)
        backtest_id = self.Create(no_overwrite_reqs=True, **_default)
        return backtest_id


    def generalized_search(self, _term:Union[float, str, int]="", **kwargs):
        """ A generalized search over """
        if _term is "":
            print(not kwargs)
            if not kwargs:
                return []
            return self.Find(**kwargs)
        return self.Find(general=_term, **kwargs)

    def find_by_episode(self, episode: str, **kwargs):
        """ Find of the orders inside of an episode """
        kwargs.get("episode", None)
        kwargs.update({"episode": episode})
        return self.Find(**kwargs)

    def find_open_orders(self):
        self.Find(status="OPEN")

    def find_by_exchange(self, exchange: str, **kwargs):
        kwargs.pop("exchange", None)
        kwargs.update({"exchange": exchange})
        return self.Find(**kwargs)

    def find_sim_trades(self, **kwargs):
        """ Find simulated trades """
        
        kwargs.pop("episode", None)
        kwargs.pop("live", None)
        
        simulated_schema = {"episode": '-live', "live": False}
        simulated_schema.update(kwargs)
        sim_trades = self.Find(**simulated_schema)
        print(sim_trades)
        return sim_trades

    def find_paper_trades(self, **kwargs):
        """ Finds all of the paper trades """
        
        kwargs.pop("episode", None)
        kwargs.pop("live", None)

        paper_schema = {"episode": 'live', "live": False}
        paper_schema.update(kwargs)
        print(paper_schema)
        paper_trades = self.Find(**paper_schema)
        print(paper_trades)


    def update_status(self, order_id:str, status:str, fill_price=None):
        if status not in self.allowed_statuses:
            raise ValueError(f"The status was not correct. Will allow {self.allowed_statuses}")
        if status is not "FILLED":
            # If it's not a filled status, we're just updating the order. 
            self.UpdateID(order_id, status=status)
            return

        assert fill_price != None
        self.UpdateID(order_id, status=status, fill_price=fill_price)

def main_order_scripts():
    from pprint import pprint
    _episode=uuid.uuid4().hex 
    _userid=uuid.uuid4().hex
    _exchange = random.choice(["binance", "coinbase", "okex"])
    _jam = Jamboree()
    
    order_search = OrderSearch()
    order_search.processor = _jam
    order_id = order_search.init(
        episode=_episode, 
        userid=_userid, 
        symbol="USD/BTC", 
        side="BUY",
        timestamp=maya.now()._epoch,
        exchange=_exchange,
        amount=100,
        init_price=random.uniform(0, 1000)
    )
    eps = order_search.Find(episode=_episode, exchange=_exchange)
    
    
    
    pprint(eps)
    print("\n\n")
    
    # Update the order status
    order_search.update_status(order_id, "CANCELLED")
    
    # Get the orders from this id
    # pprint(order_search.generalized_search("okex"))


if __name__ == "__main__":
    main_order_scripts()
