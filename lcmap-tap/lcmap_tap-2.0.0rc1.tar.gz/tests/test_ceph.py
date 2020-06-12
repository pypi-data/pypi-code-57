"""
Unit tests for lcmap_tap/storage/ceph.py
"""
from contextlib import ExitStack as does_not_raise
import pytest
from lcmap_tap.storage import ceph

chips = [(-408585, 2327805), (123456, 789012)]
x = 0
y = 1

chip_downloads = [
    # arg1, arg2, expected result
    (chips[0][x], chips[0][y], does_not_raise()),
    (chips[1][x], chips[1][y], pytest.raises(IndexError)),
]


####---- Other Tests ----####
@pytest.mark.parametrize(
    "test_config, result",
    [
        ({"s3_get_timeout": 9}, 9),
        ({"s3_get_timeout": "9"}, 9),
        ({"s3_get_timeout": 0}, 0),
        ({"s3_get_timeout": -1}, 0),
        ({"s3_get_timeout": 5.0}, 5),
    ],
)
def test_timeout(test_config, result):
    """
    Verify a valid timeout is returned.
    """
    assert ceph.load_timeout(test_config) == result


####---- String Building Tests ----####
@pytest.mark.parametrize(
    "cx, cy, grid, tile_id, proc_date, result",
    [
        (
            chips[0][x],
            chips[0][y],
            "cu",
            "014006",
            "2017-07-01",
            "json/2017/CU/014/006/cover/-408585.0/2327805.0/cover--408585.0-2327805.0-2017-07-01.json",
        ),
        (
            chips[1][x],
            chips[1][y],
            "cu",
            "014006",
            "2017-07-01",
            "json/2017/CU/014/006/cover/123456.0/789012.0/cover-123456.0-789012.0-2017-07-01.json",
        ),
    ],
)
def test_cover_key(cx, cy, grid, tile_id, proc_date, result):
    """Verify correct land cover string returned."""
    assert ceph.cover_key(cx, cy, grid, tile_id, proc_date) == result


@pytest.mark.parametrize(
    "cx, cy, result",
    [
        (chips[0][x], chips[0][y], "pixel/-408585-2327805.json"),
        (chips[1][x], chips[1][y], "pixel/123456-789012.json"),
    ],
)
def test_pixel_key(cx, cy, result):
    """Verify correct pixel string returned"""
    assert ceph.pixel_key(cx, cy) == result


@pytest.mark.parametrize(
    "cx, cy, result",
    [
        (chips[0][x], chips[0][y], "segment/-408585-2327805.json"),
        (chips[1][x], chips[1][y], "segment/123456-789012.json"),
    ],
)
def test_segment_key(cx, cy, result):
    """Verify correct segment string returned"""
    assert ceph.segment_key(cx, cy) == result


@pytest.mark.parametrize(
    "test_config, result",
    [
        (
            {"s3_url": "http://localhost:7484", "s3_bucket": "test-bucket"},
            "http://localhost:7484/test-bucket",
        ),
    ],
)
def test_bucket(test_config, result):
    """Verify correct bucket string is returned"""
    assert ceph.bucket(test_config) == result


@pytest.mark.parametrize(
    "test_config, test_key, result",
    [
        (
            {"s3_url": "http://localhost:7484", "s3_bucket": "test-bucket"},
            "segment/-408585-2327805.json",
            "http://localhost:7484/test-bucket/segment/-408585-2327805.json",
        ),
    ],
)
def test_object_key(test_config, test_key, result):
    """Verify correct object_key path is returned"""
    assert ceph.object_key(test_key, test_config) == result


####---- Download Tests ----####
@pytest.mark.parametrize(
    "cx, cy, grid, tile_id, proc_date, result",
    [
        (chips[0][x], chips[0][y], "cu", "014006", "2017-07-01", does_not_raise(),),
        (
            chips[1][x],
            chips[1][y],
            "cu",
            "014006",
            "2017-07-01",
            pytest.raises(IndexError),
        ),
    ],
)
def test_get_cover(cx, cy, grid, tile_id, proc_date, result):
    """Test a land cover product download."""
    with result:
        assert (
            ceph.get_cover(cx, cy, grid, tile_id, proc_date)[0]["primary-landcover"]
            is not None
        )


@pytest.mark.parametrize("cx, cy, result", chip_downloads)
def test_get_pixel(cx, cy, result):
    """Test a pixel file download"""
    with result:
        assert ceph.get_pixel(cx, cy)[0]["px"] is not None


@pytest.mark.parametrize("cx, cy, result", chip_downloads)
def test_get_segment(cx, cy, result):
    """Test a segment file download"""
    with result:
        assert ceph.get_segment(cx, cy)[0]["thint"] is not None
