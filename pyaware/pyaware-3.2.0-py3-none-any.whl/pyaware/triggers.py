from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
import typing
from datetime import timedelta, datetime
from pyaware import async_threaded
import pyaware.config

number = typing.Union[float, str]


class Deadline:
    def __init__(self, parameter: str, time, timestamp: datetime = datetime.utcfromtimestamp(0), dev_id: str = ""):
        self.device = dev_id
        self.parameter = parameter
        self._time = timedelta(seconds=time)
        self.timestamp = timestamp

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        self._time = timedelta(seconds=value)

    @property
    def deadline(self):
        return self.timestamp + self.time

    def tuple(self):
        return self.deadline, self.parameter, self.device

    def __le__(self, other):
        if isinstance(other, Deadline):
            return self.tuple() <= other.tuple()
        else:
            return self.tuple() <= other

    def __lt__(self, other):
        if isinstance(other, Deadline):
            return self.tuple() < other.tuple()
        else:
            return self.tuple() < other

    def __gt__(self, other):
        if isinstance(other, Deadline):
            return self.tuple() > other.tuple()
        else:
            return self.tuple() > other

    def __ge__(self, other):
        if isinstance(other, Deadline):
            return self.tuple() >= other.tuple()
        else:
            return self.tuple() >= other

    def __eq__(self, other):
        if isinstance(other, Deadline):
            return self.tuple() == other.tuple()
        else:
            return self.tuple() == other

    def __ne__(self, other):
        if isinstance(other, Deadline):
            return self.tuple() != other.tuple()
        else:
            return self.tuple() == other

    def __hash__(self):
        return id(self)

    def __repr__(self):
        return f"Deadline {self.parameter} <{self.deadline.isoformat()}> - {self.device}"


class ChangeByNothing:
    def __init__(self, param=None):
        self.parameters = set([])

    def __call__(self, reference, data: dict, timestamp: datetime):
        common = self.parameters.intersection(data)
        return {k: {timestamp: data[k]} for k in common}

    def __eq__(self, other):
        return isinstance(other, ChangeByNothing)

    def __ne__(self, other):
        return not isinstance(other, ChangeByNothing)

    def __hash__(self):
        return id(ChangeByNothing)


class ChangeOfState:
    def __init__(self, param=None):
        self.parameters = set([])

    def __call__(self, reference, data: dict, timestamp: datetime):
        common = self.parameters.intersection(data)
        resp = {}
        for key in common:
            try:
                ref = reference[key][max(reference[key])]
            except (IndexError, KeyError):
                resp[key] = {timestamp: data[key]}
                continue
            value = data[key]
            if ref != value:
                resp[key] = {timestamp: data[key]}
        return resp

    def __eq__(self, other):
        return isinstance(other, ChangeOfState)

    def __ne__(self, other):
        return not isinstance(other, ChangeOfState)

    def __hash__(self):
        return id(ChangeOfState)


class ChangeByVal:
    def __init__(self, param):
        self.value = param
        self.parameters = set([])

    def __call__(self, reference, data: dict, timestamp: datetime):
        common = self.parameters.intersection(data)
        resp = {}
        for key in common:
            try:
                ref = reference[key][max(reference[key])]
            except KeyError:
                resp[key] = {timestamp: data[key]}
                continue
            value = data[key]
            if ref - self.value < value < ref + self.value:
                continue
            resp[key] = {timestamp: data[key]}
        return resp

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False

    def __ne__(self, other):
        try:
            return self.value != other.value
        except AttributeError:
            return True

    def __hash__(self):
        return id(ChangeByVal) + self.value


class ChangeByTime:
    def __init__(self, param):
        self.time: typing.Union[int, float] = param
        self.parameters = set([])

    def __call__(self, reference: dict, data: dict, timestamp: datetime):
        common = self.parameters.intersection(data)
        resp = {}
        for key in common:
            try:
                ref = max(reference[key])
            except KeyError:
                resp[key] = {timestamp: data[key]}
                continue
            if timestamp >= ref + timedelta(seconds=self.time):
                resp[key] = {timestamp: data[key]}
        return resp

    def __eq__(self, other):
        try:
            return self.time == other.time
        except AttributeError:
            return False

    def __ne__(self, other):
        try:
            return self.time != other.time
        except AttributeError:
            return True

    def __hash__(self):
        return id(ChangeByTime) + self.time


process_trigger_types = {
    "state": ChangeOfState,
    "time": ChangeByTime,
    "value": ChangeByVal,
    "always": ChangeByNothing,
}
collect_trigger_types = {
    "deadline": Deadline
}


def nested_dict():
    return defaultdict(nested_dict)


def add_process_trigger(existing: list, param: str, trigger: str, *params):
    """
    Uses the special methods __eq__ and __ne__ on the triggers to determine if a common trigger already exists
    :return:
    """
    # Create an instance of the trigger
    trig = process_trigger_types[trigger](*params)
    # Use special methods __eq__, __ne__ on the triggers to check if this instance already exists
    if trig not in existing:
        existing.append(trig)
    # Get the already created trigger and add the parameters
    idx = existing.index(trig)
    existing[idx].parameters.add(param)


def add_collect_trigger(existing: list, param: str, trigger: str, *params):
    """
    Uses the special methods __eq__ and __ne__ on the triggers to determine if a common trigger already exists
    :return:
    """
    existing.append(collect_trigger_types[trigger](param, *params))


def build_from_device_config(path):
    """
    Builds the triggers from a configuration file
    :param path:
    :return:
    """
    parsed = pyaware.config.load_config(path)
    triggers = {"process": defaultdict(list),
                "collect": defaultdict(list)}

    for param, data in parsed["parameters"].items():
        for trig in data.get("triggers", {}).get("process", {}).get("store", []):
            add_process_trigger(triggers["process"]["store"], param, *trig)
        for trig in data.get("triggers", {}).get("process", {}).get("send", []):
            add_process_trigger(triggers["process"]["send"], param, *trig)
        for trig in data.get("triggers", {}).get("process", {}).get("event", []):
            add_process_trigger(triggers["process"]["event"], param, *trig)
        for trig in data.get("triggers", {}).get("collect", {}).get("read", []):
            add_collect_trigger(triggers["collect"]["read"], param, *trig)
    return triggers


@async_threaded
def process_triggers(reference, data, triggers, timestamp):
    processed_data = {}
    for trigger in triggers:
        processed_data.update(trigger(reference, data, timestamp))
    return processed_data


class Validator:
    pass


class Parser:
    """
    Extracts data from a topic
    """

    def __call__(self, data):
        return data


@dataclass
class DictParser:
    """

    """
    key: str = ""

    def __call__(self, data):
        if self.key:
            return data[self.key].copy()
        else:
            return data.copy()


class ValidationError(BaseException):
    pass
