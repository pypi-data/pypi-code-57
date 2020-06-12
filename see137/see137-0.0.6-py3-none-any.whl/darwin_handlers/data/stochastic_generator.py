import maya
import uuid
import dask
import copy
import random
import pandas as pd
import numpy as np
from loguru import logger
from crayons import (
    red, magenta, yellow, cyan, green
)
from typing import Optional, List

from see137.stochastic import generate_super_price
from jamboree import JamboreeNew

from jamboree.handlers.default.data import DataHandler
from jamboree.handlers.default.multi import MultiDataManagement

class PriceGenerator(object):
    def __init__(self, **kwargs) -> None:
        self._start_time = maya.now()
        self._seconds = kwargs.get("seconds", 0)
        self._minutes = kwargs.get("minutes", 0)
        self._hours = kwargs.get("hours", 0)
        self._days = kwargs.get("days", 1)
        self._months = kwargs.get("months", 0)
        self._years = kwargs.get("years", 0)
        
        self.asset_bars = {}
        self._assets = set()
        self._episodes = set()
        
        self.starting_min=50
        self.starting_max=2000
        self.is_varied=True
        self.excluded_assets=[]
        self.length=4000
        self.episode_set = {}


    @property
    def assets(self):
        return list(self._assets)
    
    @assets.setter
    def assets(self, _assets:list):
        if len(_assets) == 0:
            return
        for _ in _assets:
            self._assets.add(_)


    @property
    def start_time(self) -> 'maya.MayaDT':
        return copy.copy(self._start_time)
    
    
    
    @start_time.setter
    def start_time(self, _start_time):
        if isinstance(_start_time, float):
            # we know it's an epoch
            self._start_time = maya.MayaDT(_start_time)
        
        elif isinstance(_start_time, maya.MayaDT):
            self._start_time = _start_time
    

    @property
    def episodes(self):
        """ """
        return list(self._episodes)
    
    @episodes.setter
    def episodes(self, _episodes:List[str]):
        """ Add a list of episodes """
        if len(_episodes) == 0:
            return
        for episode in _episodes:
            self._episodes.add(episode)

    
    def generate_price_bar(self, name:str, base_type:Optional[str]=None, base_len:int=1000, base_price:float=1000.0):
        base_type = base_type or random.choice(
            ["GBM", "HESTON", "MERTON", "COX", "ORNSTEIN"]
        )
        price = generate_super_price(
            base_price=base_price,
            base_type=base_type,
            base_time=base_len
        )
        ps = len(price)
        vol_multiplier = random.uniform(2, 20)
        open_multiplier = np.absolute(np.random.normal(1, 0.03, size=ps))
        high_multiplier = np.absolute(np.random.normal(1.12, 0.03, size=ps))
        low_multiplier =  np.absolute(np.random.normal(0.92, 0.03, size=ps))
        noise = np.absolute(
            np.random.normal(1, 0.2, size=ps)
        )
    
        volume_bars = (noise * price) * vol_multiplier
        open_prices = price * open_multiplier
        high_prices = high_multiplier * price
        low_prices = low_multiplier * price

        bars = []
        start_time = self.start_time
        count = 0
        for _ in range(ps):
            bar = {
                "open": float(open_prices[_]),
                "close": float(price[_]),
                "high": float(high_prices[_]),
                "volume": float(volume_bars[_]),
                "low": float(low_prices[_]),
                "time": float((start_time.add(
                                seconds=(self._seconds * count), 
                                minutes=(self._minutes * count), 
                                hours=(self._hours * count), 
                                days=(self._days * count), 
                                months=(self._months * count), 
                                years=(self._years * count)
                )._epoch))
            }
            count += 1
            bars.append(bar)
        
        frame = pd.DataFrame(bars)
        timestamps = pd.to_datetime(frame.time, unit='s')
        frame.set_index(timestamps, inplace=True)
        frame = frame.drop(columns=["time"])
        self.asset_bars[name] = frame


    def generate(self, starting_min=50, starting_max=2000, is_varied=True, excluded_assets=[], _len=4000):
        """ Generate price bars for assets """
        assets = self.assets
        if len(assets) == 0:
            logger.error(red("No assets found"))
            return
        
        for excluded in self.excluded_assets:
            assets.remove(excluded)
        
        # Generate bars

        dask_tasks = []
        for asset in assets:
            base_price = random.uniform(self.starting_min, self.starting_max)
            _type = random.choice(
                ["GBM", "HESTON", "MERTON", "ORNSTEIN"]
            )
            dask_task = dask.delayed(self.generate_price_bar)(asset, _type, self.length, base_price)
            dask_tasks.append(dask_task)
        dask.compute(*dask_tasks)
        logger.success(f"All pricing successfully generated for episode")
        return self.asset_bars

    def generate_episode_and_set(self, episode):
        pricing_generation = self.generate()
        self.episode_set[episode] = pricing_generation
        logger.success("Finished generated episode")

    def generate_all_episodes(self):
        self.episode_set = {}
        dask_tasks = []
        for episode in self.episodes:
            dask_task = dask.delayed(self.generate_episode_and_set)(episode)
            # pricing_generation = self.generate()
            # self.episode_set[episode] = pricing_generation
            dask_tasks.append(dask_task)
        dask.compute(*dask_tasks)
        return self.episode_set

def create_data_item(category:str, subcategory:dict, name:str):
    dset = {
        "name": name,
        "subcategories": subcategory,
        "category": category
    }
    return dset

def price_gen_func():
    asset_list = ["BTC", "ATL", "TRX", "ETH", "BCH", "XRP"]
    episodes = [uuid.uuid4().hex for x in range(10)]
    price_gen = PriceGenerator()
    price_gen.episodes = episodes
    price_gen.assets = asset_list
    price_gen.starting_min = 50
    price_gen.starting_max=2000
    price_gen.is_varied=True
    price_gen.length=2000
    price_gen.generate()
    return price_gen

def price_gen_funcs(
        number_of_eps:int, 
        asset_list:List[str]=["BTC", "ATL", "TRX", "ETH", "BCH", "XRP"]) -> 'PriceGenerator':
    episodes = [uuid.uuid4().hex for x in range(number_of_eps)]
    price_gen = PriceGenerator()
    price_gen.episodes = episodes
    price_gen.assets = asset_list
    price_gen.starting_min = 50
    price_gen.starting_max=2000
    price_gen.is_varied=True
    price_gen.length=1000
    price_gen.generate_all_episodes()
    return price_gen

def set_heads(episodes:List[str], data_handler:'DataHandler', start_time:maya.MayaDT):
    if len(episodes) <= 0:
        return 
    for episode in episodes:
        logger.info(cyan(episode))
        data_handler.episode = episode
        data_handler.time.head = start_time.add(weeks=4)._epoch
        data_handler.time.change_stepsize(microseconds=0, days=1, hours=0)
        data_handler.time.change_lookback(microseconds=0, weeks=4, hours=0)



def forward_run(episodes:List[str], data_handler:'DataHandler', assets:List[str]):
    copied_episodes = copy.copy(episodes)
    copied_assets = copy.copy(assets)
    while True:
        for episode in copied_episodes:
            data_handler.episode = episode
            for asset in copied_assets:
                data_handler['name'] = asset
                if data_handler.is_next:
                    data_handler.time.step()
                else:
                    continue

def main():
    jam_processor = JamboreeNew()
    data_handler = DataHandler()
    multi_data = MultiDataManagement()
    data_handler.processor = jam_processor
    multi_data.processor = jam_processor
    episode = uuid.uuid4().hex

    start = maya.now()._epoch
    price_gen = price_gen_funcs(10)

    
    data_handler.live = False
    category = "fake_markets"
    subcategories = {
        "market": "stock",
        "country": "US",
        "sector": "faaaaake"
    }

    multi_data["set_name"] = uuid.uuid4().hex
    data_handler['category'] = category
    data_handler['subcategories'] = subcategories



    for episode in price_gen.episodes:
        all_coins = price_gen.episode_set[episode]
        coin_keys = list(all_coins['data'].keys())

        if len(coin_keys) == 0:
            return
        
        data_handler.episode = episode
        for coin in coin_keys:
            data = all_coins['data'][coin]
            data_handler['name'] = coin
            data_handler.reset()
            data_handler.store_time_df(data)
    

    set_heads(price_gen.episodes, data_handler, price_gen.start_time)
    forward_run(price_gen.episodes, data_handler, price_gen.assets)



if __name__ == "__main__":
    main()