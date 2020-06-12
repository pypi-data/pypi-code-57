import uuid
from typing import Any, Dict

from addict import Dict as ADict
from loguru import logger

from see137.common import AddictWithManagerComponent

def uhex():
    return uuid.uuid4().hex

class FindStrategyComponent(AddictWithManagerComponent):
    """Find Strategy

        Find strategy by strategy id.
    """
    def __init__(self):
        super().__init__()
        self.name = "Find Strategy"
        # Backtest configuration dict. Can be saved into the database immediately.
        self.required_items = {"strategy": str}

    def process(self, item: ADict):
        logger.critical(item)
        return item

    def step(self, item: ADict, **kwargs):
        return super().step(item, **kwargs)


if __name__ == "__main__":
    sample_backtest_dict = ADict(strategy=uhex())
    find_strategy = FindStrategyComponent()
    find_strategy.step(sample_backtest_dict, info={"one": "two"})
