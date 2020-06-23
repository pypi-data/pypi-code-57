"""
Unit tests for lcmap_tap/RetrieveData/retrieve_chips.py
"""
import datetime

# pytest - fixture decorations
import pytest

from lcmap_tap.RetrieveData import retrieve_chips


@pytest.mark.parametrize("num_days", [(8), (0), (-1)])
def test_get_acquired_dates(num_days):
    """
    Verify the correct start/end dates are returned
    """
    # initial date object for the delta calculation
    date = datetime.datetime(2017, 1, 1)

    # Test various num_days from the parametrize decorator
    start, stop = retrieve_chips.Chips.get_acquired_dates(date, num_days)

    # Values can be viewed via 'pytest -vs'
    print("\nStart date: " + str(start))
    print("Stop date: " + str(stop))

    # The start date delta must always be less than the stop date
    # in order to get a valid time series from Merlin
    assert start < stop
