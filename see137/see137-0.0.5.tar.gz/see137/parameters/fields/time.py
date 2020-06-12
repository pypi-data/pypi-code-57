import maya
import json
import time
import uuid
import datetime
from typing import Union, Optional, Any
from dataclasses import dataclass, field, fields
from jamboree.utils.core import consistent_hash
from addict import Dict as ADict


class TimeRange:
    """
        TimeRange
        ---
        A parameter to be used in remote backtesting. 
    """
    def __init__(self,
                 start: Union[str, float, int, datetime.datetime],
                 end: Union[str, float, int] = time.time(),
                 timezone: str = "UTC"):
        self.timezone = timezone
        self.start = self.HandleTimeParam(start)
        self.end = self.HandleTimeParam(end)
        self.interval = maya.MayaInterval(start=self.start, end=self.end)

    def HandleTimeParam(self, param: Union[str, float, int, datetime.datetime]):
        """Convert the parameter into a maya object. Generic time manipulation.

        Arguments:
            param {Union[str, float, int]} -- The time object epoch or string version of time

        Raises:
            ValueError: [description]

        Returns:
            [type] -- [description]
        """
        if isinstance(param, float) or isinstance(param, int):
            current_time = maya.MayaDT(param).datetime(
                to_timezone=self.timezone)
            prior_time = maya.MayaDT.from_datetime(current_time)
            return prior_time
        elif isinstance(param, str):
            return maya.when(param, timezone=self.timezone)
        elif isinstance(param, datetime.datetime):
            return maya.MayaDT.from_datetime(param)
        elif isinstance(param, datetime.date):
            return maya.when(param.isoformat(), timezone=self.timezone)
        print(type(param))
        print(isinstance(param, ))
        raise ValueError(
            f"Param is not the an acceptable datatype: [str, float, int] {type(param)}")

    def to_epoch_addict(self):
        epoch_dict = ADict()
        epoch_dict.start = self.start.epoch
        epoch_dict.end = self.end.epoch
        epoch_dict.duration = self.interval.duration
        return epoch_dict

    def to_epoch(self):
        """To Epoch
        
        Create an epoch addict dictionary carried with all of the necessary epoch information to create a backtest
        """
        epoch_dict = ADict()
        epoch_dict.start = self.start.epoch
        epoch_dict.end = self.end.epoch
        epoch_dict.duration = self.interval.duration
        return epoch_dict


class MovementSpecification:
    """ Use to deal with step information and lookback information """
    def __init__(self,
                 microseconds: float = 0,
                 seconds: float = 0,
                 minutes: float = 0,
                 hours: float = 0,
                 days: float = 0,
                 weeks: float = 0):
        self.microseconds = microseconds
        self.seconds = seconds
        self.minutes = minutes
        self.hours = hours
        self.days = days
        self.weeks = weeks

    def verify(self) -> bool:
        """Verifies that not all specified fields are not zero

        Returns:
            bool -- True if none are negative AND at least one is greater than 0
        """

        fields = [
            self.microseconds, self.seconds, self.minutes, self.hours,
            self.days, self.weeks
        ]
        return all(x >= 0 for x in fields) and any(x > 0 for x in fields)
    

    def to_dict(self):
        assert self.verify(), "At least one of the fields needs to be greater than 0, and all of them can't be negative"
        return {
            "microseconds": self.microseconds,
            "seconds": self.seconds,
            "minutes": self.minutes,
            "hours": self.hours,
            "days": self.days,
            "weeks": self.weeks
        }

    def to_json(self) -> str:
        """to_json
        
        Use to send complex information to other parts of the system. 

        Returns:
            str -- return a json string
        """
        return json.dumps(self.to_dict())

    def to_epoch(self):
        current_time = maya.now()
        next_time = maya.now()
        next_time = next_time.add(**self.to_dict())
        return next_time._epoch - current_time._epoch