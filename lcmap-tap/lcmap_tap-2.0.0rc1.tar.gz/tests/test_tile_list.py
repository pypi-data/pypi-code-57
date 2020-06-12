"""
Unit tests for lcmap_tap/RetrieveData/tile_list.py
"""
from contextlib import ExitStack as does_not_raise
import pytest
from lcmap_tap.RetrieveData import tile_list


@pytest.mark.parametrize(
    "index, index_value, length, exception",
    [
        (0, "032003", 422, does_not_raise()),
        (421, "001004", 422, does_not_raise()),
        (500, "", 422, pytest.raises(IndexError)),
    ],
)
def test_cu_tiles(index, index_value, length, exception):
    """Validate conus (cu) tile list"""
    with exception:
        assert tile_list.cu_tiles()[index] == index_value
    assert len(tile_list.cu_tiles()) == length


@pytest.mark.parametrize(
    "index, index_value, length, exception",
    [
        (0, "", 0, pytest.raises(IndexError)),
        (421, "", 0, pytest.raises(IndexError)),
        (500, "", 0, pytest.raises(IndexError)),
    ],
)
def test_ak_tiles(index, index_value, length, exception):
    """Validate alaska (ak) tile list"""
    with exception:
        assert tile_list.ak_tiles()[index] == index_value
    assert len(tile_list.ak_tiles()) == length


@pytest.mark.parametrize(
    "index, index_value, length, exception",
    [
        (0, "", 0, pytest.raises(IndexError)),
        (421, "", 0, pytest.raises(IndexError)),
        (500, "", 0, pytest.raises(IndexError)),
    ],
)
def test_hi_tiles(index, index_value, length, exception):
    """Validate hawaii (hi) tile list"""
    with exception:
        assert tile_list.hi_tiles()[index] == index_value
    assert len(tile_list.hi_tiles()) == length
