import maya
import uuid
from typing import Union, Optional
# import see137.parameters.fields i
from see137.parameters.fields import TimeRange, MovementSpecification
from jamboree.handlers.default import TimeHandler
from jamboree.utils.core import consistent_hash
from see137.parameters.parameter import Parameter
from loguru import logger

class TimeParameter(Parameter):
    def __init__(self, interval:TimeRange, steps:MovementSpecification, lookback:MovementSpecification, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interval = interval
        self.stepinfo = steps
        self.lbinfo = lookback
        if not isinstance(self.interval, TimeRange):
            raise ValueError("Interval needs to be a time range")
        if not isinstance(self.stepinfo, MovementSpecification):
            raise ValueError("Steps configuration data needs to be a RangeSpecificField.")
        if not isinstance(self.lbinfo, MovementSpecification):
            raise ValueError("Lookback parameters supplied needs to be RangeSpecificField.")
    
    @property
    def start(self) -> float:
        """Return the starting epoch

        Returns:
            float -- the epoch for the start of the backtest. Set the head to this
        """
        return self.interval.start.epoch

    @property
    def end(self) -> float:
        """Return the ending epoch

        Returns:
            float -- the epoch for the end of the backtest. Check for this at the end of steps for multiple assets. 
        """
        return self.interval.end.epoch
    
    @property
    def step(self) -> str:
        """Return Step Size Information

        Returns:
            str -- string describing how much we're going to be moving the observation needle ahead.
        """
        return self.stepinfo.to_json()
    
    @property
    def lookback(self) -> str:
        """Return Lookback Size Information

        Returns:
            str -- string describing how much we're going to be looking backwards during the backtest.
        """
        return self.lbinfo.to_json()
    
    @property
    def duration(self):
        return self.interval.interval.duration
    

@logger.catch
def main():
    start = "2007-05-02"
    end = "2020-04-22"
    timezone = "UTC"
    interval = TimeRange(start=start, end=end, timezone=timezone)
    steps = MovementSpecification(days=2)
    lookback = MovementSpecification(weeks=2)

    

    time_conf = TimeParameter(interval=interval, steps=steps, lookback=lookback)
    print(time_conf.start)
    print(time_conf.end)
    print(time_conf.lookback)
    print(time_conf.step)
    print(time_conf.duration)


if __name__ == "__main__":
    main()