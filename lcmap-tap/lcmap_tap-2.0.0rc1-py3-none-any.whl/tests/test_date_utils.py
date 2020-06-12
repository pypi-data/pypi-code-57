"""
Unit tests for lcmap_tap/date_utils.py
"""
import pytest
from cytoolz import first
from cytoolz import last
from lcmap_tap import date_utils


@pytest.mark.parametrize(
    "date_start, date_end, length",
    [("1985-07-01", "2017-07-01", 33),],
)
def test_gen_dates(date_start, date_end, length):
    """Validate processing date list generation."""
    proc_dates = date_utils.gen_dates(date_start, date_end)
    print(proc_dates)
    assert first(proc_dates) == date_start
    assert last(proc_dates) == date_end
    assert len(proc_dates) == length


@pytest.mark.parametrize(
    "dates, result", [(["1985-07-01", "1986-07-01", "1987-07-01"], "1985-07-01"),],
)
def test_gen_sday_eday(dates, result):
    """Validate generated start/end date list."""
    date_list = date_utils.gen_sday_eday(dates)
    print(f"date_list is: {date_list}")
    assert first(date_list)["sday"] == result


@pytest.mark.parametrize(
    "dates, result",
    [(["1985-07-01", "1986-07-01", "1987-07-01"], ("1985-07-01", "1986-07-01")),],
)
def test_sday_eday_pairs(dates, result):
    """Validate start ane end date pairs."""
    date_pairs = date_utils.sday_eday_pairs(dates)
    print(f"date_pairs are: {date_pairs}")
    assert first(date_pairs) == result


@pytest.mark.parametrize(
    "dates, result",
    [([("1985-07-01", "1986-07-01"), ("1986-07-01", "1987-07-01")], "1985-07-01"),],
)
def test_sday_eday_dict(dates, result):
    """Validate the start/end date list of dictionaries."""
    sedays = list(map(date_utils.sday_eday_dict, dates))
    print(f"sedays are: {sedays}")
    assert first(sedays)["sday"] == result
