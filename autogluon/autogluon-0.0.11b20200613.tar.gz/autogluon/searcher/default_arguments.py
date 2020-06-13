from typing import Set, Tuple, Dict
import logging
import numbers

logger = logging.getLogger(__name__)


class CheckType(object):
    def assert_valid(self, key: str, value):
        pass


class Float(CheckType):
    def __init__(self, lower: float = None, upper: float = None):
        if lower and upper:
            assert lower < upper
        self.lower = lower
        self.upper = upper

    def assert_valid(self, key: str, value):
        assert isinstance(value, numbers.Real), \
            "{}: Value = {} must be of type float".format(key, value)
        assert (not self.lower) or value >= self.lower, \
            "{}: Value = {} must be >= {}".format(key, value, self.lower)
        assert (not self.upper) or value <= self.upper, \
            "{}: Value = {} must be <= {}".format(key, value, self.upper)


class Integer(CheckType):
    def __init__(self, lower: int = None, upper: int = None):
        if lower and upper:
            assert lower < upper
        self.lower = lower
        self.upper = upper

    def assert_valid(self, key: str, value):
        assert isinstance(value, numbers.Integral), \
            "{}: Value = {} must be of type int".format(key, value)
        assert (not self.lower) or value >= self.lower, \
            "{}: Value = {} must be >= {}".format(key, value, self.lower)
        assert (not self.upper) or value <= self.upper, \
            "{}: Value = {} must be <= {}".format(key, value, self.upper)


class Categorical(CheckType):
    def __init__(self, choices: Tuple[str, ...]):
        self.choices = set(choices)

    def assert_valid(self, key: str, value):
        assert isinstance(value, str) and value in self.choices, \
            "{}: Value = {} must be in {}".format(key, value, self.choices)


class Boolean(CheckType):
    def assert_valid(self, key: str, value):
        assert isinstance(value, bool), \
            "{}: Value = {} must be boolean".format(key, value)


def check_and_merge_defaults(
        options: dict, mandatory: Set[str], default_options: dict,
        constraints: Dict[str, CheckType]=None, dict_name=None) -> dict:
    """
    First, check that all keys in mandatory appear in options. Second, create
    result_options by merging options and default_options, where entries in
    options have precedence. Finally, if constraints is given, this is used to
    check validity of values.

    :param options:
    :param mandatory:
    :param default_options:
    :param constraints:
    :return: result_options
    """
    prefix = "" if dict_name is None else "{}: ".format(dict_name)
    for key in mandatory:
        assert key in options, \
            prefix + "Key '{}' is missing (but is mandatory)".format(key)
    log_msg = ""
    result_options = options.copy()
    for key, value in default_options.items():
        if key not in options:
            log_msg += (prefix + "Key '{}': Imputing default value {}\n".format(
                key, value))
            result_options[key] = value
    if log_msg:
        logger.info(log_msg)
    # Check constraints
    if constraints:
        for key, value in result_options.items():
            check = constraints.get(key)
            if check:
                check.assert_valid(prefix + "Key '{}'".format(key), value)

    return result_options
