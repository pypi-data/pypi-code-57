import uuid
from typing import Dict, Any
from addict import Dict as ADict
from see137.common import ComponentAbstract, AddictWithManagerComponent


class DecideStrategyComponent(AddictWithManagerComponent):
    """Decide Strategy

        Pull strategy from the database and make decision
    """
    def __init__(self):
        super().__init__()
        self.name = "Decide Strategy"
        # Backtest configuration dict. Can be saved into the database immediately.
        self.required_items:Dict[str, type] = {"strategy_blob":object, "episode": str, "data" : object}

        # Make sure the data is already pulled (We'll probably be casting this into a dataframe)
        # self.required_settings: Dict[str, type] = {}
    
    def process(self, item:ADict):
        strategy_blob = item.strategy_blob
        # Check strategy type (leave out for now)
        preprocessed_data = strategy_blob.preprocess(item)
        action, percentage = strategy_blob.step(preprocessed_data)
        item.action = action
        item.percentage = percentage

    def step(self, item:ADict, **kwargs):
        return super().__init__(item, **kwargs)