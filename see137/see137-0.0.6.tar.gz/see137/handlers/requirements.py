import time
import random
import uuid
import copy
from typing import List, Dict, Any, Set
from loguru import logger
from jamboree import Jamboree
from jamboree.handlers.default import DBHandler
from jamboree.handlers.default import MultiDataManagement
from jamboree.utils.helper import Helpers
from pprint import pprint


helpers = Helpers()


class RequirementsHandler(DBHandler):
    """ 
        # RequirementsHandler
        ---

        This manages the required items before moving onto the next step. 

        This is poorly written. Will likely rewrite it for more accuracy and speed.
    """

    def __init__(self):
        super().__init__()
        self.entity = "requirements"
        self.required = {
            "name": str,
            "live": bool,
            "episode": str
        }
        self['episode'] = "normal"
        self['live'] = True
        self.is_unique = False

        self._data = MultiDataManagement()
        self._episode: str = uuid.uuid4().hex
        self._live: bool = False
        self._assets: List[Dict[Any, Any]] = []
        self._items_compressed: Set[str] = set()
        self._reporting = {}

    @property
    def episode(self):
        return self._episode

    @episode.setter
    def episode(self, _episode):
        self._episode = _episode

    @property
    def live(self):
        return self._live

    @live.setter
    def live(self, _live):
        self._live: bool = _live

    @property
    def sources(self):
        """ Using multi-data for it validity checks. """
        name = self['name']
        episode = self['episode']
        live = self['live']
        self._data['name'] = f"{name}-{episode}-{live}"
        self._data['category'] = "assistance"
        self._data['subcategories'] = {}
        self._data['submetatype'] = "requirement"
        self._data['abbreviation'] = "REQMAN"
        self._data.episode = episode
        self._data.live = live
        self._data.processor = self.processor
        return self._data

    def unique(self):
        """ Get the requirements specified to the episode and live status"""
        unique_item = RequirementsHandler()
        unique_item['name'] = self['name']
        unique_item['episode'] = self.episode
        unique_item['live'] = self.live
        unique_item.assets = self.assets
        unique_item.episode = self.episode
        unique_item.processor = self.processor
        unique_item.is_unique = True
        unique_item.reset()
        return unique_item

    def asset_update(self, items: List[Dict[Any, Any]], command="add"):
        if len(items) == 0:
            return

        if command not in ["add", "sub"]:
            return

        _current_items = set()

        [_current_items.add(helpers.generate_hash(x)) for x in items]
        old_items = self.items
        if command == "add":
            old_items = old_items.union(_current_items)
        else:
            old_items = old_items.difference(_current_items)

        self.items = old_items
        # self.assets = self.decomp_items
        self.update()


    @property
    def assets(self):
        return self._assets

    @assets.setter
    def assets(self, _assets):
        self._assets = _assets
        self.assets_to_items()

    @property
    def items(self) -> Set:
        return self._items_compressed

    @items.setter
    def items(self, _items: Set[str]):
        self._items_compressed = _items

    @property
    def decomp_items(self):
        if len(self.items) == 0:
            return []
        return [helpers.hash_to_dict(x) for x in self.items]

    @property
    def is_valid(self):
        self.items = set(self._reporting.keys())
        self._general_update()

        report_values = list(self._reporting.values())
        if len(report_values) == 0:
            return False
        return all(report_values)


    def assets_to_items(self):
        _item_list = set()
        for asset in self.assets:
            _item_list.add(helpers.generate_hash(asset))
        self._items_compressed = _item_list

    def _unique_update(self):
        """ Adds the episode if this is an episode specific requirements """

        asset_list = []
        for asset in self.assets:
            if 'subcategories' in asset:
                asset['subcategories']['episode'] = self.episode
            else:
                asset['episode'] = self.episode
            asset_list.append(asset)
        self.assets = asset_list

    def default_reporting(self):
        self.prune_reports()

        for item in self.items:
            self._reporting[item] = self._reporting.get(item, False)

    def prune_reports(self):
        current_reports = copy.copy(self._reporting)
        for key in current_reports:
            if key not in self.items:
                self._reporting.pop(key, None)

    def reset_reports(self):
        """ Set the reporting to False and save"""
        for key in self._reporting.keys():
            self._reporting[key] = False
        self.update()

    def _general_update(self):

        self.assets = self.decomp_items
        self.default_reporting()

    """ Core functions """
    def report(self, asset: Dict[Any, Any]):
        """ Report that we've passed over an asset """
        self.load()
        itemized = helpers.generate_hash(asset)
        self._reporting[itemized] = True
        self.update()

    def load(self):
        """ Load all of the assets and the status of those assets as well """
        asset_set = self.last()

        report_set = self.last(alt={"detail": "report"})
        self.assets = asset_set.get("assets", [])
        self._reporting = report_set.get("report", {})
        if self.is_unique:
            self._unique_update()
            self.assets_to_items()
        self._general_update()

    def update(self):
        if self.is_unique:
            self._unique_update()
            self.assets_to_items()
        self._general_update()

        data = {"assets": self.assets,
                "time": time.time(), "timestamp": time.time()}

        report = {"report": self._reporting,
                  "time": time.time(), "timestamp": time.time()}
        self.save(data)
        self.save(report, alt={"detail": "report"})

    def count_assets(self) -> int:
        """Get count of assets that are required in this session.

        Returns:
            int -- Required Asset Cardinality
        """
        # This should be cached at some point
        current_count = self.get_single(alt={"detail": "cardinal_count"})
        if bool(current_count):
            return
        # logger.success(current_count)
        return len(self.assets)

    def count_cardinality(self):
        return self.count(alt={"detail": "cardinal"})

    def report_cardinality(self, asset: dict):
        self.save({"asset": asset}, alt={"detail": "cardinal"})

    def flush_cardinality(self):
        self.delete_all(alt={"detail": "cardinal"})

    @property
    def is_valid_cardinality(self) -> bool:
        """Detects if the asset cardinality matches the current number of assets.

        Returns:
            bool -- [description]
        """
        current_count = self.count_cardinality()
        total_asset_count = self.count_assets()
        # logger.info(current_count)
        # logger.info(total_asset_count)
        return (current_count >= total_asset_count)

    def reset(self):
        self.sources.reset()
        req_count = self.count()
        if req_count == 0:
            pass
            # logger.debug("Updating for the first time")

            self.update()
        else:
            self.load()

    def info(self):
        return {
            "episode": self.episode,
            "is_unique": self.is_unique
        }


if __name__ == "__main__":

    all_assets = ["BTC", "XTZ", "ETH", "ATX",
                  "XRP", "BCH", "BSV", "LTC", "EOS"]

    jambo = Jamboree()
    reqhandler = RequirementsHandler()
    reqhandler.processor = jambo
    # The name is on rick and morty so it's not perverted. I can prove it
    reqhandler['name'] = "PoopybuttholeS"
    reqhandler.assets = [
        {
            "name": x,
            "category": "market",
            "subcategories": {"exchange": "fake_exchange"}
        }
        for x in all_assets
    ]
    reqhandler.reset()
    new_items = [
        {
            "name": x,
            "category": "market",
            "subcategories": {"exchange": "fake_exchange"}
        }
        for x in ["ONE", "TWO", "THREE", "FOUR", "BTC", "ATX"]
    ]
    reqhandler.asset_update(new_items, command="sub")
    reqhandler.reset()

    assets = reqhandler.assets
    while True:
        current_asset = random.choice(assets)
        # logger.info(current_asset)
        reqhandler.report_cardinality(current_asset)
        # logger.success(reqhandler.is_valid_cardinality)
        if reqhandler.is_valid_cardinality:
            logger.debug("Episode step is done")
            logger.success("Pushing the time step forward")
            reqhandler.flush_cardinality()
        else:
            logger.warning("Not done yet")
            logger.error("Handling next step")
