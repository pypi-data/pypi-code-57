# -*- coding: utf-8 -*-
# Copyright (c) 2016 - 2020 Sqreen. All rights reserved.
# Please refer to our terms for more information:
#
#     https://www.sqreen.io/terms.html
#
"""Sanitizer used to remove sensitive data from our payload"""

import json
import logging
import re

from . import config
from .utils import HAS_TYPING, flatten, is_string, is_unicode

if HAS_TYPING:
    from typing import (
        AbstractSet,
        Any,
        FrozenSet,
        Iterable,
        Iterator,
        Mapping,
        MutableMapping,
        Pattern,
        Set,
        Tuple,
    )
else:
    from collections import Iterable, Mapping


LOGGER = logging.getLogger(__name__)

MASK = '<Redacted by Sqreen>'


def compile_sensitive_regex():
    # type: () -> Pattern[str]
    try:
        pattern = config.CONFIG["STRIP_SENSITIVE_REGEX"]
        if not isinstance(pattern, str):
            raise TypeError
        return re.compile(pattern)
    except (TypeError, re.error):
        LOGGER.warning("Invalid regexp configuration: %r", config.CONFIG["STRIP_SENSITIVE_REGEX"])
        pattern = config.CONFIG_DEFAULT_VALUE["STRIP_SENSITIVE_REGEX"]
        if not isinstance(pattern, str):
            raise TypeError("Invalid default regex configuration")
        return re.compile(pattern)


SENSITIVE_KEYS = frozenset([k.strip() for k in config.CONFIG["STRIP_SENSITIVE_KEYS"].split(',')])  # type: FrozenSet[str]
SENSITIVE_VALUES = frozenset()  # type: FrozenSet[str]
SENSITIVE_REGEX = compile_sensitive_regex()
LOGGER.debug("Using sensitive keys %s", ", ".join(SENSITIVE_KEYS))
LOGGER.debug("Using sensitive regex %s", SENSITIVE_REGEX.pattern)


def sanitize(data, sensitive_keys=SENSITIVE_KEYS,
             sensitive_regex=SENSITIVE_REGEX,
             sensitive_values=SENSITIVE_VALUES):
    # type: (Any, AbstractSet[str], Pattern[str], AbstractSet[str]) -> Tuple[Any, AbstractSet[str]]
    """
    Sanitize sensitive data from an object. Return a 2-tuple with a sanitized
    copy of the data and a list of values that were sanitized.
    """
    sensitive_data = set()  # type: Set[str]

    if is_string(data):
        if not is_unicode(data):
            data = data.decode("utf-8", errors="replace")
        if data in sensitive_values or sensitive_regex.search(data):
            sensitive_data.add(data)
            data = MASK
        return data, sensitive_data

    elif isinstance(data, Mapping):
        new_dict = {}
        for k, v in data.items():
            if k in sensitive_keys:
                new_dict[k] = MASK
                if is_string(v):
                    sensitive_data.add(v)
                elif isinstance(v, Iterable):
                    keys, values = flatten(v)
                    sensitive_data.update(keys)
                    sensitive_data.update(values)
            else:
                ret_data, child_sensitive_data = sanitize(
                    v, sensitive_keys=sensitive_keys,
                    sensitive_regex=sensitive_regex,
                    sensitive_values=sensitive_values)
                new_dict[k] = ret_data
                sensitive_data.update(child_sensitive_data)
        return new_dict, sensitive_data

    elif isinstance(data, Iterable):
        new_list = []
        for v in data:
            ret_data, child_sensitive_data = sanitize(
                v, sensitive_keys=sensitive_keys,
                sensitive_regex=sensitive_regex,
                sensitive_values=sensitive_values)
            new_list.append(ret_data)
            sensitive_data.update(child_sensitive_data)
        return new_list, sensitive_data

    return data, sensitive_data


def sanitize_attacks(attacks, sensitive_values,
                     sensitive_regex=SENSITIVE_REGEX):
    # type: (Iterable[MutableMapping], AbstractSet[str], Pattern[str]) -> Iterator[MutableMapping]
    """
    Sanitize sensitive data from a list of attacks. Return the sanitized
    attacks.
    """
    for attack in attacks:
        infos = attack.get("infos")
        if infos is None:
            continue

        waf_data = infos.get("waf_data")
        if waf_data is not None:
            try:
                if isinstance(waf_data, bytes):
                    waf_data = waf_data.decode("utf-8", errors="replace")
                waf_data = json.loads(waf_data)
                assert isinstance(waf_data, list)
            except (UnicodeDecodeError, ValueError, AssertionError):
                waf_data = []

            normalized_sensitive_values = \
                {values.lower() for values in sensitive_values}
            new_waf_data = []
            for item in waf_data:
                filters = item.get("filter")
                if filters is not None:
                    for filter_item in filters:
                        resolved_value = filter_item.get("resolved_value")
                        if resolved_value is not None \
                                and resolved_value.lower() \
                                in normalized_sensitive_values:
                            filter_item["match_status"] = MASK
                            filter_item["resolved_value"] = MASK
                new_waf_data.append(item)

            infos["waf_data"] = json.dumps(new_waf_data, separators=(",", ":"))
        else:
            attack["infos"], _ = sanitize(
                infos, sensitive_keys=frozenset(),
                sensitive_regex=sensitive_regex,
                sensitive_values=sensitive_values)

        yield attack


def sanitize_exceptions(exceptions, sensitive_values):
    # type: (Iterable[Mapping], AbstractSet[str]) -> Iterator[Mapping]
    """
    Sanitize sensitive data from a list of exceptions. Return the sanitized
    exceptions.
    """
    for exc in exceptions:
        infos = exc.get("infos")
        if infos is not None:
            # We know the request contains PII, never send args
            # TODO more fine grained filtering
            args = infos.get("args")
            if args is not None and sensitive_values:
                infos.pop("args", None)

            waf_infos = infos.get("waf")
            if waf_infos is not None and sensitive_values:
                waf_infos.pop("args", None)

        yield exc
