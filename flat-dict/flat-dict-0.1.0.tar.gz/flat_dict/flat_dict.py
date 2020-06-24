from typing import Any, Dict
from collections import OrderedDict

from .constants import \
    VERSION_KEY, \
    PRIMITIVE_TYPES, \
    SUPPORTED_VERSIONS


from .utils import is_valid_key, ns_to_key, key_to_ns, get_separator, encode_value, decode_value, is_valid_version
from .exceptions import InvalidKeyError

DEFAULT_SEPARATOR = '['
DEFAULT_VERSION = '1.0'

__all__ = [
    'encode',
    'decode'
]


def encode(obj: dict, separator: str = DEFAULT_SEPARATOR, preserve_order: bool = False, version: str = DEFAULT_VERSION, *args, **kwargs) -> dict:
    # check input type
    if not isinstance(obj, dict):
        raise ValueError("The input object must be of type dict. Got {0} instead.".format(
            str(type(obj))
        ))
    # check separator
    _ = get_separator(separator)
    # check version
    if version not in SUPPORTED_VERSIONS:
        raise ValueError('Version not supported. Valid choices are: {0}'.format(
            ', '.join(SUPPORTED_VERSIONS)
        ))
    # ----
    res = OrderedDict() if (isinstance(obj, OrderedDict) or preserve_order) else dict()
    res[VERSION_KEY] = version

    def _processor(e: Any, ns=None):
        # arguments
        if ns is None:
            ns = []
        # dict-like objects
        if isinstance(e, dict):
            for k, v in e.items():
                if not is_valid_key(k, separator):
                    raise InvalidKeyError(k, ns, separator)
                _processor(v, ns + [k])
        # list-like objects
        elif isinstance(e, (list, set)):
            for i, v in enumerate(e):
                _processor(v, ns + [i])
        # primitive objects
        elif e is None or isinstance(e, tuple(PRIMITIVE_TYPES)):
            res[ns_to_key(ns, separator)] = encode_value(e)
        # invalid type
        else:
            raise ValueError("Objects of type {0} cannot be serialized".format(str(type(e))))

    _processor(obj)
    return res


def decode(d: dict, separator: str = DEFAULT_SEPARATOR, preserve_order: bool = False) -> Dict[str, str]:
    if not isinstance(d, dict):
        raise ValueError("Input must be of type 'dict', got '{0}' instead.".format(str(type(d))))
    _ = get_separator(separator)
    # ---
    # check fd version
    if VERSION_KEY not in d or not is_valid_version(d[VERSION_KEY]):
        raise ValueError(
            "Input must be a dictionary containing (at least) a valid flat-dict "
            "signature key '{0}'. Supported versions are: {1}".format(
                VERSION_KEY, ', '.join(SUPPORTED_VERSIONS)
            ))
    # ---
    res = OrderedDict()

    # any key generates its corresponding ns path in res, preferred structure is dict
    for key, value in d.items():
        if key == VERSION_KEY:
            continue
        # ---
        ns = key_to_ns(key, separator)
        if len(ns) <= 0:
            continue
        # ---
        # create structure for ns in res
        cursor = res
        for lvl in ns[:-1]:
            if lvl not in cursor:
                cursor[lvl] = OrderedDict()
            cursor = cursor[lvl]
        # place value at the end of ns
        cursor[ns[-1]] = decode_value(value)

    # some structures re-created as dicts were actually lists, find and fix them
    def fix_list(obj: Any) -> Any:
        if isinstance(obj, dict):
            keys = set(obj.keys())
            list_keys = set(range(len(obj)))
            if len(keys.intersection(list_keys)) == len(obj):
                # this dict has all numbers between 0 and N-1 as keys, turn it into a list
                return [obj[i] for i in sorted(keys)]
        return obj

    # replace ordereddict with dict
    def fix_dict(obj: Any) -> Any:
        if isinstance(obj, OrderedDict) and not preserve_order:
            return dict(obj)
        return obj

    # recursively fix lists
    def _processor(e: Any):
        # dict-like objects
        if isinstance(e, dict):
            for k in list(e.keys()):
                _processor(e[k])
                v = fix_list(e[k])
                e[k] = v if isinstance(v, list) else fix_dict(e[k])
    _processor(res)

    return fix_dict(res)
