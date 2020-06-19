#!/usr/bin/env python
"""
Name: Rio Atmadja
Date: 26 May 2020
Description: Helper class for orion-ml-engines
"""
import re
from ml_engines.utils.constants import MONTHS
def as_date(date_fmt: str) -> str:
    """
    Helper function to format date in YYYY-MM-DD
    :date_fmt: given the date format
    :return: a string in YYYY-MM-DD format
    """

    validate_date: Match = re.search(r"[a-z]{1,} [0-9]{1,2},\ {1,}[0-9]{4}",
                                     date_fmt.lower())  # validate date date format
    if not validate_date:
        raise ValueError("ERROR: Must be in format MM DD, YYYY")

    fmt_dates, fmt_year = tuple(date_fmt.split(','))
    month, day = tuple(fmt_dates.split(' '))
    day = "0" + day if int(day) < 10 else day

    return f"{fmt_year}-{MONTHS.get(month)}-{day}".strip()