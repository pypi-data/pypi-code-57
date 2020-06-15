import json
from typing import Union, Tuple
import numpy as np
from worker.data.api import API
from worker.data.enums import EventTypes


def gather_wits_for_period(asset_id: int, start: int, end: int, limit: int = 1800) -> list:
    """
    Get the wits data from API for an asset over an interval
    :param asset_id: asset id
    :param start: start timestamp
    :param end: end timestamp
    :param limit: count of the data
    :return: a list of wits data
    """
    if start >= end:
        return []

    query = '{timestamp#gte#%s}AND{timestamp#lte#%s}' % (start, end)
    worker = API()
    wits_dataset = worker.get(
        path="/v1/data/corva", collection='wits', asset_id=asset_id, sort="{timestamp: 1}", limit=limit, query=query
    ).data

    if not wits_dataset:
        return []

    return wits_dataset


def get_one_wits_record(asset_id: int, timestamp_sort: int = -1) -> dict:
    """
    Get the first or last wits record of a given asset
    :param asset_id:
    :param timestamp_sort:
    :return:
    """
    api_worker = API()
    data = api_worker.get(path='/v1/data/corva/', collection='wits', asset_id=asset_id,
                          sort="{timestamp:%s}" % timestamp_sort, limit=1).data
    if not data:
        return {}

    return data[0]


def delete_collection_data_of_asset_id(asset_id: int, collections: Union[str, list]):
    """
    Delete all the data of a collection for an asset id.
    :param asset_id:
    :param collections: a collection or a list of collections
    :return:
    """
    worker = API()

    if isinstance(collections, str):
        collections = [collections]

    for collection in collections:
        path = "/v1/data/corva/%s" % collection
        query = "{asset_id#eq#%s}" % asset_id
        worker.delete(path=path, query=query)


def is_number(data):
    """
    Check and return True if data is a number, else return False
    :param data: Input can be string, number or nan
    :return: True or False
    """
    try:
        data_cast = float(data)
        if data_cast >= 0 or data_cast <= 0:  # to make sure it is a valid number
            return True

        return False
    except ValueError:
        return False
    except TypeError:
        return False


def is_finite(data):
    """
    Check if the given data is a finite number
    Note that the string representation of a number is not finite
    :param data:
    :return: True or False
    """
    try:
        return is_number(data) and np.isfinite(data)
    except (TypeError, ValueError):
        return False


def is_int(s: str) -> bool:
    """
    To check if the given string is an integer or not
    :param s:
    :return:
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def to_number(data):
    """
    Check and return if the data can be cast to a number, else return None
    :param data: Input can be string, number or nan
    :return: A numbers
    """
    if is_number(data):
        return float(data)

    return None


def none_to_nan(data):
    """
    If data is a list, return list with None replaced with nan.
    If data is None, return nan
    :param data:
    :return:
    """
    if isinstance(data, list):
        return [np.nan if e is None else e for e in data]

    if data is None:
        return np.nan

    return data


def get_data_by_path(data: dict, path: str, func=lambda x: x, default=None):
    """
    To find the path to a key in a nested dictionary.
    Note that none of the keys should end up in a list
    :param data:
    :param path: path to the final key; example of the paths are:
        'data.X.Y'
        'data.bit_depth'
    :param func: the type of the data (int, str, float, ...)
    :param default: default value if the path not found
    :return:
    """
    if not path:
        if default is not None:
            return default

        raise KeyError("No key provided")

    keys = path.split('.')

    while keys:
        current_key = keys.pop(0)

        if current_key not in data:
            if default:
                return default

            raise KeyError("{0} not found in path".format(current_key))

        data = data.get(current_key)

    return func(data)


def is_in_and_not_none(d: dict, key: str):
    """
    An structured way of getting data from a dict.
    :param d: the dictionary
    :param key:
    :return: True or False
    """
    if key in d.keys() and d[key] is not None:
        return True

    return False


def nanround(value, decimal_places=2):
    """
    Similar to python built-in round but considering None values as well
    :param value:
    :param decimal_places:
    :return:
    """
    if is_number(value):
        return round(value, decimal_places)

    return None


def merge_dicts(d1: dict, d2: dict) -> dict:
    """
    Merge two dictionaries
    Note: the 2nd item (d2) has a higher priority to write items with similar keys
    :param d1:
    :param d2:
    :return:
    """
    d = {**d1, **d2}
    return d


def get_cleaned_event_and_type(event) -> Tuple[Union[list, dict], EventTypes]:
    """
    validate and flatten the events and organize the data into a desired format

    Task and generic events format is : dict => {}
    Scheduler events format is: list of list of dict => [[{}]]
    Kafka events format is: list of dict => [{}]
    The above formats can be used to determine the format

    :param event: a scheduler of kafka stream
    :return: event and event_type
    """

    if not event:
        raise ValueError("Empty events")

    if isinstance(event, (str, bytes, bytearray)):
        event = json.loads(event)

    if isinstance(event, dict):
        if "asset_id" in event:
            return event, EventTypes.GENERIC

        if "task_id" in event:
            return event, EventTypes.TASK

        raise TypeError("Missing task_id or asset_id keys in event")

    if not isinstance(event, list):
        raise TypeError("Event is not a list or a dict")

    first_event = event[0]
    if isinstance(first_event, list):
        if first_event[0] and "schedule_start" in first_event[0]:
            return event, EventTypes.SCHEDULER

        raise Exception("Missing scheduler_start key in scheduler event")

    elif isinstance(first_event, dict):
        # new kafka stream format: list of json objects, each with metadata and records
        # event = [{"metadata": { ... }, "records": [ ... ]}, {"metadata": { ... }, "records": [ ... ]}]
        return event, EventTypes.STREAM

    raise TypeError("Event is not either a scheduler or kafka consumer")
