"""
date_utils - Functions for transforming data structures of dates.
"""
import arrow
from cytoolz import first
from cytoolz import last
from cytoolz import second
from cytoolz import sliding_window


def gen_dates(date_start, date_end):
    """
    Generate a list of dates.
    Args:
      date_start: The starting date. (YYYY-MM-DD)
      date_end: The ending date, inclusive. (YYYY-MM-DD)
    Returns: A list of date strings in ISO8601 YYYY-MM-DD format.
    """
    start = arrow.get(date_start)
    end = arrow.get(date_end)
    years = range(start.year, end.year + 1)
    dates = []

    for y in years:
        pred_date = arrow.Arrow(year=y, month=int(start.month), day=int(start.day))
        if start <= pred_date <= end:
            dates.append(pred_date.date().isoformat())
    return dates


def gen_sday_eday(dates):
    """
    Generate a list of dictionaries for start/end dates.
    Args:
      dates: A list of dates in 'YYYY-MM-DD' format.
    Returns:
      A list of dictionaries with start/end day key pairs.
      [{"sday": YYYY-MM-DD, "eday": YYYY-MM-DD}, ]
    """
    date_pairs = sday_eday_pairs(dates)
    return list(map(sday_eday_dict, date_pairs))


def sday_eday_pairs(dates):
    """
    Build a list of start/end date pairs, using the current and next list values.
    Args:
      dates: A list of dates in 'YYYY-MM-DD'.
    Returns: A list of tuples with dates (YYYY-MM-DD) in
             format [(sday, eday), (sday, eday)].
    """
    # Start/end pairs includes all but the last pair.
    date_pairs = list(sliding_window(2, dates))

    # Retrieve the last pair dates for determining a new pair to append
    first_last_pair = arrow.get(first(last(date_pairs)))
    sec_last_pair = arrow.get(second(last(date_pairs)))

    # Determine the next end date from the last pair's year delta
    pair_diff_years = sec_last_pair.year - first_last_pair.year
    next_date_year = sec_last_pair.year + pair_diff_years

    # Add the month/day to the determined year. ("-MM-DD")
    next_date = arrow.get(
        year=next_date_year, month=sec_last_pair.month, day=sec_last_pair.day
    )

    date_pairs.append((sec_last_pair.date().isoformat(), next_date.date().isoformat()))
    return date_pairs


def sday_eday_dict(dates):
    """
    Transform a tuple of start/end dates into a dictionary.
      (ie: add keys to tuple values)
    Args:
      dates: A tuples with dates in format (YYYY-MM-DD, YYYY-MM-DD).
    Returns: A dictionary with the "sday" and "eday" keys
             added for each date value. {"sday": YYYY-MM-DD, "eday": YYYY-MM-DD}
    """
    seday = ("sday", "eday")
    return dict(zip(seday, dates))
