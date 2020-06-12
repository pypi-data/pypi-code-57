"""
Unit tests for lcmap_tap/RetrieveData/grids.py
"""
from contextlib import ExitStack as does_not_raise
import pytest
from lcmap_tap.RetrieveData import grids


##-- User Facing Functions --##
@pytest.mark.parametrize(
    "name, result",
    [
        ("cu", does_not_raise()),
        ("ak", does_not_raise()),
        ("hi", does_not_raise()),
        ("nothere", pytest.raises(AssertionError)),
    ],
)
def test_list_grids(name, result):
    """Validate the grid list"""
    with result:
        assert name in grids.list_grids()


##-- Grid Functions --##
@pytest.mark.parametrize(
    "grid, dataset, result, exception",
    [
        ("cu", "ard", "tile", does_not_raise()),
        ("space", "nothing", "stars", pytest.raises(KeyError)),
    ],
)
def test_tile_grid(grid, dataset, result, exception):
    """Validate tile grid information returned."""
    with exception:
        tile_grid_data = grids.tile_grid(grid=grid, dataset=dataset)
        print(f"tile_grid_data is: {tile_grid_data}")
        assert tile_grid_data["name"] == result


@pytest.mark.parametrize(
    "grid, dataset, result, exception",
    [
        ("cu", "ard", "chip", does_not_raise()),
        ("space", "nothing", "stars", pytest.raises(KeyError)),
    ],
)
def test_chip_grid(grid, dataset, result, exception):
    """Validate chip grid information returned."""
    with exception:
        chip_grid_data = grids.chip_grid(grid=grid, dataset=dataset)
        print(f"chip_grid_data is: {chip_grid_data}")
        assert chip_grid_data["name"] == result


@pytest.mark.parametrize(
    "grid, dataset, result, exception",
    [
        ("cu", "ard", "tile", does_not_raise()),
        ("space", "nothing", "stars", pytest.raises(KeyError)),
    ],
)
def test_grid_info(grid, dataset, result, exception):
    """Validate returned grid info dictionary."""
    with exception:
        grid_data = grids.grid_info(grid=grid, dataset=dataset)
        print(f"grid_data is: {grid_data}")
        assert grid_data[0]["name"] == result


@pytest.mark.parametrize(
    "grid, dataset, result", [("cu", "ard", [100, 100]),],
)
def test_registry_info(grid, dataset, result):
    """Validate registry layer information."""
    reg_info = grids.registry_info(grid, dataset)
    print(reg_info[0]["data_shape"])
    assert reg_info[0]["data_shape"] == result


@pytest.mark.parametrize(
    "grid, dataset, coords, result, exception",
    [
        ("cu", "ard", {"x": 2084415.0, "y": 2414805.0}, 2084415.0, does_not_raise()),
        ("cu", "ard", {"x": 2084455.0, "y": 2414855.0}, 2084415.0, does_not_raise()),
        (
            "cu",
            "ard",
            {"x": 1234567.8, "y": 9012345.6},
            2084415.0,
            pytest.raises(AssertionError),
        ),
        (
            "cu",
            "ard",
            {"x": -9999999.9, "y": -9999999.9},
            2084415.0,
            pytest.raises(AssertionError),
        ),
    ],
)
def test_snap_info(grid, dataset, coords, result, exception):
    """Validate snapped tile data."""
    tile_info = grids.snap_info(grid=grid, dataset=dataset, coords=coords)
    print(f"tile_info is: {tile_info['tile']['proj-pt'][0]}")
    with exception:
        assert tile_info["tile"]["proj-pt"][0] == result


##-- Coordinate Systems Functions --##
@pytest.mark.parametrize(
    "test, result",
    [
        ("PROJCS", does_not_raise()),
        ("standard_parallel", does_not_raise()),
        ("Albers_Conic_Equal_Area", does_not_raise()),
        ('EPSG","9122', pytest.raises(AssertionError)),
    ],
)
def test_coord_system_meters(test, result):
    """Validate string WKT for Albers Equal Area WGS 84 projected meters."""
    with result:
        assert test in grids.coord_system_meters("cu", "ard")


@pytest.mark.parametrize(
    "test, result",
    [
        ("GEOGCS", does_not_raise()),
        ('EPSG","9122', does_not_raise()),
        ("degree", does_not_raise()),
        ("Albers_Conic_Equal_Area", pytest.raises(AssertionError)),
    ],
)
def test_coord_system_geo(test, result):
    """Validate string WKT for WGS 84 geographic."""
    with result:
        assert test in grids.coord_system_geo("cu", "ard")


##-- String Generation Functions --##
@pytest.mark.parametrize(
    "test_config, result",
    [
        (
            {"ard_base_url": "http://ard-base.org", "ard_cu": "ard_cu_v01"},
            "http://ard-base.org",
        ),
    ],
)
def test_base_url(test_config, result):
    """Validate a returned base url"""
    assert grids.base_url(test_config) == result


@pytest.mark.parametrize(
    "test_config, grid, dataset, result",
    [
        (
            {"ard_base_url": "http://ard-base.org", "ard_cu": "ard_cu_v01"},
            "cu",
            "ard",
            "ard_cu_v01",
        ),
    ],
)
def test_url_path(test_config, grid, dataset, result):
    """Validate the returned url path"""
    assert grids.url_path(test_config, grid, dataset) == result


@pytest.mark.parametrize(
    "test_config, obj_key, result",
    [
        (
            {"ard_base_url": "http://ard-base.org", "ard_cu": "ard_cu_v01"},
            "ard_cu_v01/grid",
            "http://ard-base.org/ard_cu_v01/grid",
        ),
    ],
)
def test_object_key(test_config, obj_key, result):
    """Validate the full path to an object."""
    assert grids.object_key(obj_key, test_config) == result
