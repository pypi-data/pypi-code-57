import re

from types import SimpleNamespace
from typing import List, Any

from .constants import VERSION_KEY, KEY_SEPARATOR, PRIMITIVE_TYPES, PRIMITIVE_ENCODINGS, \
    PRIMITIVE_TYPE_ENCODING, PRIMITIVE_TYPE_ENCODER, PRIMITIVE_TYPE_DECODER, SUPPORTED_VERSIONS
from .exceptions import FormatError


def is_valid_version(version: str) -> bool:
    return version in SUPPORTED_VERSIONS


def is_valid_key(key: str, separator: str) -> bool:
    sep = get_separator(separator)
    return (key != VERSION_KEY) \
        and (not isinstance(key, str) or (
            (len(sep.open) <= 0 or sep.open not in key) and
            (len(sep.close) <= 0 or sep.close not in key)
        )
     )


def ns_to_key(ns: List[Any], separator: str):
    sep = get_separator(separator)
    return ''.join(map(lambda e: '{0}{1}{2}'.format(sep.open, encode_value(e), sep.close), ns))


def key_to_ns(key: str, separator: str) -> List[Any]:
    sep = get_separator(separator)
    pattern = '{0}([^{1}]+){2}'.format(
        re.escape(sep.open), re.escape(sep.close), re.escape(sep.close)
    )
    return list(map(decode_value, re.findall(pattern, key)))


def get_separator(sep: str) -> SimpleNamespace:
    if sep not in KEY_SEPARATOR:
        raise ValueError("The given separator was not recognized, "
                         "possible choices are '{0}'".format("', '".join(KEY_SEPARATOR.keys())))
    return KEY_SEPARATOR[sep]


def encode_value(value: Any) -> str:
    if not isinstance(value, tuple(PRIMITIVE_TYPES)):
        raise ValueError("Objects of type {0} cannot be serialized".format(str(type(value))))
    # ---
    encoding = PRIMITIVE_TYPE_ENCODING[type(value)]
    return '{0}:{1}'.format(encoding, str(PRIMITIVE_TYPE_ENCODER[encoding](value)))


def decode_value(encoded_value: str) -> Any:
    if len(encoded_value) <= 2:
        raise FormatError(encoded_value, 0, list(map(lambda s: s + ':', PRIMITIVE_ENCODINGS)))
    if encoded_value[0] not in PRIMITIVE_ENCODINGS:
        raise FormatError(encoded_value, 0, PRIMITIVE_ENCODINGS)
    if encoded_value[1] != ':':
        raise FormatError(encoded_value, 1, ':')
    # ---
    encoding, str_value = encoded_value[0], encoded_value[2:]
    # ---
    return PRIMITIVE_TYPE_DECODER[encoding](str_value)
