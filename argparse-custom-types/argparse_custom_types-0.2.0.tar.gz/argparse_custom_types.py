""" argparse custom types"""
import argparse

from typing import Callable
from typing import List
from typing import Tuple
from typing import Union


def int_range(start: int, stop: int, step: int = 1) -> Callable:
    """ custom int in range from start to stop (not including)."""
    excepted_range = [x for x in range(start, stop, step)]

    def _int_range(value: str) -> int:
        error_msg = f"{value} is an invalid int value in " \
                    f"range {start} - {stop - 1}"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value not in excepted_range:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value

    return _int_range


def int_above(minimum: int) -> Callable:
    """ int equal to or above minimum. """

    def _int_above(value: str) -> int:
        error_msg = f"{value} is an invalid int value above {minimum}"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value < minimum:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value
    return _int_above


def int_below(maximum: int) -> Callable:
    """ int equal to or below maximum. """

    def _int_below(value: str) -> int:
        error_msg = f"{value} is an invalid int value below {maximum}"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value > maximum:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value
    return _int_below


def int_even(pos_number: bool = True,
             neg_number: bool = False,
             include_zero: bool = False,
             ) -> Callable:
    """ even int value """

    def _int_even(value: str) -> int:
        error_msg = f"{value} is an invalid even int"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value == 0 and not include_zero:
                raise argparse.ArgumentTypeError(error_msg)
            elif int_value < 0 and not neg_number:
                raise argparse.ArgumentTypeError(error_msg)
            elif int_value > 0 and not pos_number:
                raise argparse.ArgumentTypeError(error_msg)
            elif int_value % 2 != 0:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value
    return _int_even


def int_odd(pos_number: bool = True,
            neg_number: bool = False,
            include_zero: bool = False,
            ) -> Callable:
    """ odd int value """

    def _int_odd(value: str) -> int:
        error_msg = f"{value} is an invalid odd int"
        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        else:
            if int_value < 0 and not neg_number:
                raise argparse.ArgumentTypeError(error_msg)
            elif int_value > 0 and not pos_number:
                raise argparse.ArgumentTypeError(error_msg)
            elif int_value == 0 and include_zero:
                return int_value
            elif int_value % 2 == 0:
                raise argparse.ArgumentTypeError(error_msg)
            else:
                return int_value
    return _int_odd


def in_sequence_strings(sequence: Union[Tuple[str], List[str]],
                        show_on_invalid: bool = False,
                        case_sensitive: bool = True,
                        ) -> Callable:
    """
    excepts a value that is in the tuple or list and returns
    that value as a string

    show_on_invalid = True will show a list of acceptable values

    case_sensitive = False will convert to lower case then check if
    value is in the sequence
    """
    seq_string = ", ".join(sequence)
    if not case_sensitive:
        sequence = [x.lower() for x in sequence]

    def _in_sequence_strings(value: str) -> str:
        if not case_sensitive:
            value = value.lower()

        msg = f"{value} is not in the excepted value list"

        if show_on_invalid:
            error_msg = f"{msg}\n{seq_string}"
        else:
            error_msg = msg

        if value in sequence:
            return value
        else:
            raise argparse.ArgumentTypeError(error_msg)

    return _in_sequence_strings


def in_sequence_ints(sequence: Union[List[int], Tuple[int]],
                     show_on_invalid: bool = False) -> Callable:
    """
    excepts an int value that is in the sequence

    show_on_invalid = True will show a list on invalid value.
    """
    str_sequence = ", ".join([str(x) for x in sequence])

    def _in_sequence_ints(value: str) -> int:
        msg = f"{value} is not in the excepted int value list"

        if show_on_invalid:
            error_msg = f"{msg} {str_sequence}"
        else:
            error_msg = msg

        try:
            int_value = int(value)
        except ValueError:
            raise argparse.ArgumentTypeError(error_msg)
        if int_value in sequence:
            return int_value
        else:
            raise argparse.ArgumentTypeError(error_msg)

    return _in_sequence_ints
