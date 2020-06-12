"""
Unit tests for lcmap_tap/RetrieveData/retrieve_ccd.py
"""
from contextlib import ExitStack as does_not_raise
from collections import namedtuple
import pytest
from lcmap_tap.RetrieveData import retrieve_ccd

GeoCoordinate = namedtuple("GeoCoordinate", ["x", "y"])

chips = [(-408585, 2327805), (123456, 789012)]
pixels = [(-408585, 2324835), (123456, 789012)]
x = 0
y = 1

chip_downloads = [
    # chip_coord, pixel_coord, expected result
    (
        GeoCoordinate(chips[0][x], chips[0][y]),
        GeoCoordinate(pixels[0][x], pixels[0][y]),
        does_not_raise(),
    ),
    (
        GeoCoordinate(chips[1][x], chips[1][y]),
        GeoCoordinate(pixels[1][x], pixels[1][y]),
        pytest.raises(IndexError),
    ),
]

prediction_test_data = [
    {
        "cx": -408585,
        "cy": 2327805,
        "px": -408585,
        "py": 2324835,
        "sday": "1984-05-23",
        "eday": "1987-07-26",
        "pday": "1984-07-01",
        "prob": [
            2.2908416830169642e-10,
            0.20634277164936066,
            0.003137607127428055,
            0.7905178070068359,
            1.3163719891906567e-08,
            4.130397428525612e-07,
            1.4040946325621917e-06,
            2.2908416830169642e-10,
            7.04995661848784e-09,
        ],
    },
    {
        "cx": -408585,
        "cy": 2327805,
        "px": -408585,
        "py": 2324865,
        "sday": "1982-12-04",
        "eday": "1987-08-11",
        "pday": "1983-07-01",
        "prob": [
            1.8768306353500464e-10,
            0.0010448329849168658,
            0.008290804922580719,
            0.990662157535553,
            5.67067388601572e-08,
            2.555516118718515e-07,
            1.8822261154127773e-06,
            1.8768306353500464e-10,
            4.107041107204168e-08,
        ],
    },
]

date_range = [
    "1985-07-01", "1986-07-01", "1987-07-01", "1988-07-01", "1989-07-01",
    "1990-07-01", "1991-07-01", "1992-07-01", "1993-07-01", "1994-07-01",
    "1995-07-01", "1996-07-01", "1997-07-01", "1998-07-01", "1999-07-01",
    "2000-07-01", "2001-07-01", "2002-07-01", "2003-07-01", "2004-07-01",
    "2005-07-01", "2006-07-01", "2007-07-01", "2008-07-01", "2009-07-01",
    "2010-07-01", "2011-07-01", "2012-07-01", "2013-07-01", "2014-07-01",
    "2015-07-01", "2016-07-01", "2017-07-01"]


@pytest.mark.parametrize(
    "chip_coord, result",
    [
        # get the same file twice (1st from ceph, then from cache)
        (GeoCoordinate(chips[0][x], chips[0][y]), does_not_raise()),
        (GeoCoordinate(chips[0][x], chips[0][y]), does_not_raise()),
        (GeoCoordinate(chips[1][x], chips[1][y]), pytest.raises(IndexError)),
    ],
)
def test_get_cache_or_ceph(chip_coord, result):
    """
    Test getting a chip from ceph and cache.
    """
    with result:
        assert retrieve_ccd.get_cache_or_ceph("pixel", chip_coord)[0] is not None


@pytest.mark.parametrize(
    "chip_coord, grid, tile_id, proc_dates, length, exception",
    [
        (
            GeoCoordinate(chips[0][x], chips[0][y]),
            "cu",
            "014006",
            date_range,
            33,
            does_not_raise(),
        ),
    ],
)
def test_get_cover_range(
    chip_coord, grid, tile_id, proc_dates, length, exception
):
    """
    Test getting land cover products for a chip.
    """
    cover = retrieve_ccd.get_cover_range(
        chip_coord, grid, tile_id, proc_dates
    )
    print(f"cover: {cover[0][0]} \nlength: {len(cover)}")
    with exception:
        assert cover[0][0]["primary-landcover"] is not None
        assert len(cover) == length


@pytest.mark.parametrize(
    "chip_cover, px_index, result1, result2",
    [
        (
            [
                [
                    {
                        "primary-landcover": 3,
                        "secondary-landcover": 1,
                        "primary-confidence": 82,
                        "secondary-confidence": 16,
                        "annual-change": 3,
                    },
                    {
                        "primary-landcover": 1,
                        "secondary-landcover": 3,
                        "primary-confidence": 90,
                        "secondary-confidence": 1,
                        "annual-change": 1,
                    },
                ],
                [
                    {
                        "primary-landcover": 4,
                        "secondary-landcover": 1,
                        "primary-confidence": 95,
                        "secondary-confidence": 10,
                        "annual-change": 3,
                    },
                    {
                        "primary-landcover": 1,
                        "secondary-landcover": 3,
                        "primary-confidence": 90,
                        "secondary-confidence": 1,
                        "annual-change": 1,
                    },
                ],
            ],
            0,
            3,
            4,
        ),
    ],
)
def test_filter_pixels_cover(chip_cover, px_index, result1, result2):
    """Validate the filtering of a pixel out of a list of chips"""
    pixel_cover = retrieve_ccd.filter_pixels_cover(chip_cover, px_index)
    print(f"pixel_cover: {pixel_cover}")
    assert pixel_cover[0]["primary-landcover"] == result1
    assert pixel_cover[1]["primary-landcover"] == result2


@pytest.mark.parametrize(
    "chip_coord, pixel_coord, year_start, year_stop, length, exception",
    [
        (
            GeoCoordinate(chips[0][x], chips[0][y]),
            GeoCoordinate(pixels[0][x], pixels[0][y]),
            "1985-07-01",
            "2017-07-01",
            33,
            does_not_raise(),
        ),
    ],
)
def test_get_ccd_cover(
    chip_coord, pixel_coord, year_start, year_stop, length, exception
):
    """
    Test getting land cover products down to a specific pixel.
    """
    cover = retrieve_ccd.get_ccd_cover(chip_coord, pixel_coord, year_start, year_stop)
    print(f"cover (first): {cover[0]} \nlength: {len(cover)}")
    with exception:
        assert cover[0]["primary-landcover"] is not None
        assert len(cover) == length


@pytest.mark.parametrize("chip_coord, pixel_coord, result", chip_downloads)
def test_get_ccd_pixel_mask(chip_coord, pixel_coord, result):
    """
    Test getting a ccd pixel mask list.
    """
    with result:
        assert retrieve_ccd.get_ccd_pixel_mask(chip_coord, pixel_coord)[0] is not None


@pytest.mark.parametrize("chip_coord, pixel_coord, result", chip_downloads)
def test_get_ccd_segment(chip_coord, pixel_coord, result):
    """
    Test getting a segment model for a chip.
    """
    with result:
        assert (
            retrieve_ccd.get_ccd_segment(chip_coord, pixel_coord)[0]["thint"]
            is not None
        )


@pytest.mark.parametrize(
    "chip, pixel_coord, result",
    [
        (
            prediction_test_data,
            GeoCoordinate(pixels[0][x], pixels[0][y]),
            does_not_raise(),
        ),
        (
            prediction_test_data,
            GeoCoordinate(pixels[1][x], pixels[1][y]),
            pytest.raises(IndexError),
        ),
    ],
)
def test_pixel_ccd_info(chip, pixel_coord, result):
    """
    Test finding a specific pixel from a chip json object.
    """
    with result:
        assert retrieve_ccd.pixel_ccd_info(chip, pixel_coord)[0]["prob"] is not None
