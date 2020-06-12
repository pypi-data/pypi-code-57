import uuid
import pandas as pd
import numpy as np
import maya
from jamboree import Jamboree, DBHandler
from jamboree.handlers.default import TimeHandler

from loguru import logger
from typing import List, Dict, Any, Optional
from cytoolz.itertoolz import pluck

from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from pypfopt.efficient_frontier import EfficientFrontier

logger.disable(__name__)
"""
    Note: Will remove soon. Going through a concept.
"""




class AllocationHandler(DBHandler):
    """Abstract handler that we use to keep track of information.
    """

    def __init__(self, limit=500, spacing=5, unit="hours"):
        super().__init__()
        self.entity = "allocation"
        self.required = {
            "user_id": str,
            "exchange": str,
            "episode": str,
            "live": bool
        }
        self._balance = 0
        self._limit = limit
        self._spacing = spacing
        self._unit = unit
        self._time:Optional[TimeHandler] = None
    
        
    
    # -------------------------------------------------------------------
    # --------------------- Properties & Setters ------------------------
    # -------------------------------------------------------------------
    


    @property
    def limit(self):
        return self._limit
    
    @limit.setter
    def limit(self, limit):
        self._limit = limit
    

    @property
    def spacing(self):
        return self._spacing

    @spacing.setter
    def spacing(self, space):
        self._spacing = space


    @property
    def time(self):
        if self._time is None:
            raise AttributeError("Time not found")
        return self._time
    

    @time.setter
    def time(self, _time:TimeHandler):
        self._time = _time

    """
        Notes:
            TODO: Change how the units are done.
    """

    @property
    def unit(self):
        
        return self._unit
    
    @unit.setter
    def unit(self, _unit):
        self._unit = _unit


    @property
    def assets(self) -> list:
        """ Get all of the assets that we're watching for the exchange """
        return self.latest_asset().get("assets", [])

    @property
    def allocation(self):
        return self.latest_allocation().get("allocation", {})
    
    @property
    def current_step(self):
        alt = {"detail": "steps"}
        count = self.count(alt=alt)
        return count
    
    @property
    def last_time(self):
        _late = self.latest_timestamp()
        
        return _late.get("epoch", maya.now()._epoch)

    @property
    def should_rebalance(self) -> bool:
        """ Depending on the scenario, we determine if we should rebalance."""
        """
            if live:
                check if the determined amount of time has passed since we've rebalanced
            else:
                check if the predetermined number of steps have happened.
        """
        if self["live"]:
            current_epoch = maya.now()._epoch
            expected = maya.MayaDT(self.last_time).add(**{f"{self.unit}":self.spacing})._epoch
            if current_epoch >= expected:
                
                return True
        else:
            if self.current_step % self.spacing == 0:
                return True
        return False

    def latest_asset(self):
        alt = {"detail": "assets"}
        asset = self.last(alt=alt)
        return asset
    
    def latest_allocation(self):
        alt = {"detail": "allocation"}
        asset = self.last(alt=alt)
        return asset
    

    def latest_timestamp(self):
        alt = {"detail": "timestamp"}
        asset = self.last(alt=alt)
        return asset


    def timestamp_count(self) -> int:
        """ Get the count of the asset adds we have. Not the number of assets. """
        alt = {"detail": "timestamp"}
        count = self.count(alt=alt)
        return count

    
    def asset_count(self) -> int:
        """ Get the count of the asset adds we have. Not the number of assets. """
        alt = {"detail": "assets"}
        count = self.count(alt=alt)
        return count
    


    def count_steps(self):
        alt = {"detail": "steps"}
        count = self.count(alt=alt)
        return count

        
    
    def save_allocation(self, allocation:dict):
        """ Save monitored assets """
        alt = {"detail": "allocation"}
        monitored = {
            "allocation": allocation,
            "time": self.time.head
        }
        self.save(monitored, alt=alt)
    
    def save_timestamp(self, _time=None):
        """ Save monitored assets """
        if _time is None:
            _time = maya.now()._epoch
        alt = {"detail": "timestamp"}
        monitored = {
            "epoch": _time
        }
        self.save(monitored, alt=alt)


    def save_step(self):
        alt = {"detail": "steps"}
        monitored = {}
        self.save(monitored, alt=alt)
    







    def _filter_assets(self, all_assets:dict) -> dict:
        assets = self.assets
        users_portfolio_to_rebalance = {}
        _all_assets = all_assets.get("assets", None)
        if _all_assets is None:
            return {}
        for asset in assets:
            current_asset = _all_assets.get(asset, None)
            if current_asset is not None:
                users_portfolio_to_rebalance[asset] = current_asset

        return users_portfolio_to_rebalance
    

    def _extract_frame(self, portfolio_assets:dict):
        time_is_filled = False
        time_index = []
        portfolio_close = {}
        for asset in portfolio_assets.keys():
            current_pricing = portfolio_assets.get(asset, [])
            portfolio_close[asset] = list(pluck("close", current_pricing))
            if time_is_filled == False:
                time_index = list(pluck("time", current_pricing))
                time_is_filled = True
        
        pandas_index = pd.to_datetime(time_index, unit='s')
        pclose = pd.DataFrame(portfolio_close, index=pandas_index)
        return pclose

    

    


    def _finish_step(self, is_rebalance=False):
        """ Finish update that we're not """
        if is_rebalance == True:
            # Give a timestamp of the last rebalance.
            self.save_timestamp()
        self.save_step()
        


    # def step(self, all_assets:Dict[str, Any]) -> None:
    #     """ Accept all of the assets for a given allocation and begin"""
        

    #     if self.should_rebalance == True:
    #         users_portfolio_to_rebalance = self._filter_assets(all_assets)

    #         portfolio_keys = users_portfolio_to_rebalance.keys()
    #         if len(portfolio_keys) == 0:
    #             logger.info(magenta("There are no portfolio keys", bold=True))
    #             self._finish_step()
    #             return

    #         pclose = self._extract_frame(users_portfolio_to_rebalance)
    #         self.mean_variance_opt.allocate(pclose)
    #         current_allocation = self.mean_variance_opt.weights.to_dict('records')[0]
    #         logger.info(current_allocation)
    #         self.save_allocation(current_allocation)
    #         self._finish_step(is_rebalance=True)
    #         return

    #         # Set timestamp aka, the last time we did a rebalance.
    #     self._finish_step()

    

    def step(self, rebal_frame:pd.DataFrame) -> None:
        """ Accept all of the assets for a given allocation and begin"""
        
        # logger.info(rebal_frame)
        rebal_len = len(rebal_frame)
        if rebal_len == 0:
            # Don't rebalance any further
            self._finish_step()
            return

        if self.should_rebalance == True:
            # Set timestamp aka, the last time we did a rebalance
            mu = mean_historical_return(rebal_frame)
            S = CovarianceShrinkage(rebal_frame).ledoit_wolf()
            logger.info(S)
            ef = EfficientFrontier(mu, S)
            weights = ef.max_sharpe()
            current_allocation = ef.clean_weights()
            converted_allocation = {}
            for k, v in current_allocation.items():
                if isinstance(v, np.generic):
                    converted_allocation[k] = v.item()
                    continue
                converted_allocation[k] = v
            self.save_allocation(converted_allocation)
            self._finish_step(is_rebalance=True)


        self._finish_step()
    

    def new_step_test(self, rebal_frame:pd.DataFrame) -> None:
        """ Accept all of the assets for a given allocation and begin"""
        

        rebal_len = len(rebal_frame)
        if rebal_len == 0:
            # Don't rebalance any further
            self._finish_step()
            return

        if self.should_rebalance == True:
            # Set timestamp aka, the last time we did a rebalance
            mu = mean_historical_return(rebal_frame)
            S = CovarianceShrinkage(rebal_frame).ledoit_wolf()
            ef = EfficientFrontier(mu, S)
            weights = ef.max_sharpe()
            logger.info(weights)
            current_allocation = ef.clean_weights()
            self.save_allocation(current_allocation)
            self._finish_step(is_rebalance=True)


        self._finish_step()


    def rebalance(self, rebalance_dataframe:pd.DataFrame):
        logger.info(rebalance_dataframe)


    def _reset_timestamp(self):
        if self.timestamp_count() == 0:
            self.save_timestamp(_time=maya.when('12 years ago')._epoch)


    def reset(self):
        self._reset_timestamp()


def experiment_main():
    jam = Jamboree()


if __name__ == "__main__":
    experiment_main()