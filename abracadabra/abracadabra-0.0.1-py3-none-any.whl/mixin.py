#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections.abc import Sequence, Mapping
import json
from pandas import DataFrame
import numpy as np

BIG = 2.**32
SMALL = -2.**32
# TYPE_MAPPING = {np.inf: BIG, -np.inf: SMALL, np.nan: SMALL}  # uclear what the best choice is here
TYPE_MAPPING = {np.inf: None, -np.inf: None, np.nan: None}  # uclear what the best choice is here


class InitRepr(object):
    """
    __repr__ returns intialization command
    """
    def __repr__(self):
        class_name = self.__class__.__name__
        class_len = len(class_name)
        attr_str = ["{}={!r}".format(attr, getattr(self, attr)) for attr in self.__ATTRS__]
        attr_str = ",\n{}".format(" " * (1 + class_len)).join(attr_str)
        return f"{class_name}({attr_str})"


class Jsonable(object):
    """
    Allows object ot be converted to a json string
    """

    def to_json(self):
        return json.dumps(self, default=lambda x: x.__dict__,
                          sort_keys=True, indent=4)

    def __repr__(self):
        return self.to_json()


class Dataframeable(object):
    """
    Export a set of attributes tabular format. Must implement a `json` property
    method that returns a dict-like with the following structure (i.e. that
    supported by pandas for generating a single-row dataframe from JSON):

        {"FIELD_1_NAME": [FIELD_1_VALUE],
         "FIELD_2_NAME": [[FIELD_2_VALUE_A, FIELD_2_VALUE_B]],
         "FIELD_3_NAME": [(FIELD_3_VALUE_A, FIELD_3_VALUE_B)], ...
         }
    """
    @property
    def json(self):
        raise NotImplementedError('Must implement json property')

    def to_dataframe(self, safe_cast=False):
        """
        Export result to a dataframe. If `safe_cast` is True attempt to
        casting common problematic values (see TYPE_MAPPING); this can be useful
        for ensuring type safety, for example when uploading data to a database.
        """
        _json = self.json
        if safe_cast:
            _json = _safe_cast_json(_json, TYPE_MAPPING)
        return DataFrame(_json)


def safe_isnan(val):
    if val is not None:
        return np.isnan(val)
    return False


def _safe_cast_json(data, mapping):
    """
    Apply safe casting of common problem data types (see TYPE_MAPPING).
    """
    _apply = lambda x: _safe_cast_json(x, mapping)
    if isinstance(data, (str, bool)):
        return data
    elif isinstance(data, Mapping):
        return type(data)({k: _apply(v) for k, v in list(data.items())})
    elif isinstance(data, Sequence):
        # # additional sequence processing, no None in sequences
        # _data = [_apply(v) for v in data]
        # _data = [d if d is not None else 0 for d in _data]
        return type(data)(_apply(v) for v in data)
    else:
        return mapping.get(data, data) if not safe_isnan(data) else mapping[np.nan]
