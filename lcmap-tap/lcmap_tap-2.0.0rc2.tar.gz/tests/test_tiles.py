"""
Unit tests for lcmap_tap/RetrieveData/tiles.py
"""
from contextlib import ExitStack as does_not_raise
import pytest
from lcmap_tap.RetrieveData import tiles


##-- User Facing Functions --##
@pytest.mark.parametrize(
    "grid, length", [("cu", 422), ("ak", 0), ("hi", 0),],
)
def test_list_tiles(grid, length):
    """Validate the listing of tiles."""
    assert len(tiles.list_tiles(grid)) == length


@pytest.mark.parametrize(
    "grid, dataset, result",
    [
        (
            "cu",
            "ard",
            {
                "length": 422,
                "h": 32,
                "v": 3,
                "tile_ul": {"x": -66.88687358195142, "y": 45.66670475157042},
                "tile_ll": {"x": -67.45610994454883, "y": 44.38016421334179},
            },
        ),
    ],
)
def test_hv_longlat(grid, dataset, result):
    """Validate the hv_longlat list."""
    hv_longlat = tiles.hv_longlat(grid, dataset)
    print(hv_longlat[0])
    assert len(hv_longlat) == result["length"]
    assert hv_longlat[0][0]["h"] == result["h"]
    assert hv_longlat[0][0]["v"] == result["v"]
    assert hv_longlat[0][1]["tile_ul"] == result["tile_ul"]
    assert hv_longlat[0][1]["tile_ll"] == result["tile_ll"]


@pytest.mark.parametrize(
    "grid, dataset, tile_id, result, exception",
    [
        ("cu", "ard", "031006", {"x": 2084415.0, "y": 2414805.0}, does_not_raise()),
        ("cu", "ard", "1", {}, pytest.raises(ValueError)),
    ],
)
def test_tile_to_xy(grid, dataset, tile_id, result, exception):
    """Validate tile id to x,y coordinate conversion."""
    with exception:
        assert tiles.to_xy(grid, dataset, tile_id) == result


@pytest.mark.parametrize(
    "grid, dataset, coords, result",
    [
        ("cu", "ard", {"x": 2084415.0, "y": 2414805.0}, "031006"),
        ("cu", "ard", {"x": 2084415.0, "y": 2414801.0}, "031006"),
        ("cu", "ard", {"x": -408585, "y": 2327805}, "014006"),
    ],
)
def test_xy_to_tile(grid, dataset, coords, result):
    """Validate x,y to tile id conversion."""
    assert tiles.xy_to_tile(grid, dataset, coords) == result


@pytest.mark.parametrize(
    "grid, dataset, pixel_coords, result",
    [
        ("cu", "ard", {"x": 2084415.0, "y": 2414805.0}, 0),
        ("cu", "ard", {"x": 2084455.0, "y": 2414805.0}, 1),
        ("cu", "ard", {"x": 2084415.0, "y": 2414775.0}, 100),
        ("cu", "ard", {"x": 0, "y": 0}, 9369),
        ("cu", "ard", {"x": 2084415.0, "y": 0}, 9350),
        ("cu", "ard", {"x": 0, "y": 2414805.0}, 19),
        ("cu", "ard", {"x": -2084415.0, "y": 2414805.0}, 39),
        ("cu", "ard", {"x": 2084415.0, "y": -2414805.0}, 8700),
    ],
)
def test_pixel_index(grid, dataset, pixel_coords, result):
    """Validate a pixel index from a flattened chip array."""
    pixel_pos = tiles.pixel_index(grid, dataset, pixel_coords)
    print(pixel_pos)
    assert pixel_pos == result


@pytest.mark.parametrize(
    "grid, dataset, result", [("cu", "ard", (3000.0, 3000.0)),],
)
def test_chip_size(grid, dataset, result):
    """Validate a grid's chip size."""
    chip_info = tiles.chip_size(grid, dataset)
    print(chip_info)
    assert chip_info == result


@pytest.mark.parametrize(
    "grid, dataset, result", [("cu", "ard", (30.0, 30.0)),],
)
def test_pixel_size(grid, dataset, result):
    """Validate a grid's pixel size."""
    pixel_info = tiles.pixel_size(grid, dataset)
    print(pixel_info)
    assert pixel_info == result


@pytest.mark.parametrize(
    "grid, dataset, coords, src, dest, result",
    [
        (
            "cu",
            "ard",
            {"x": 2084415.0, "y": 2414805.0},
            "meters",
            "latlong",
            {"x": -70.28444796560534, "y": 42.18008415854808},
        ),
    ],
)
def test_convert_xy_latlong(grid, dataset, coords, src, dest, result):
    """Validate converting x,y coordinates to geo long,lat."""
    assert tiles.convert_xy_latlong(grid, dataset, coords, src, dest) == result


@pytest.mark.parametrize(
    "grid, dataset, tile_xy, result",
    [
        (
            "cu",
            "ard",
            {"x": 2084415.0, "y": 2414805.0},
            {
                "tile_ul": {"x": 2084415.0, "y": 2414805.0},
                "tile_ur": {"x": 2234415.0, "y": 2414805.0},
                "tile_lr": {"x": 2234415.0, "y": 2264805.0},
                "tile_ll": {"x": 2084415.0, "y": 2264805.0},
            },
        ),
    ],
)
def test_tile_xy_corners(grid, dataset, tile_xy, result):
    """Validate x,y corner coordinate generation."""
    assert tiles.xy_corners(grid, dataset, tile_xy) == result


@pytest.mark.parametrize(
    "grid, dataset, tile_corners, src, dest, result",
    [
        (
            "cu",
            "ard",
            {
                "tile_ul": {"x": 2084415.0, "y": 2414805.0},
                "tile_ur": {"x": 2234415.0, "y": 2414805.0},
                "tile_lr": {"x": 2234415.0, "y": 2264805.0},
                "tile_ll": {"x": 2084415.0, "y": 2264805.0},
            },
            "meters",
            "latlong",
            {
                "tile_ul": {"x": -70.28444796560534, "y": 42.18008415854808},
                "tile_ur": {"x": -68.53211953437867, "y": 41.809734073605895},
                "tile_lr": {"x": -69.04107230807199, "y": 40.524467436607495},
                "tile_ll": {"x": -70.76420061777073, "y": 40.88766599493269},
            },
        ),
    ],
)
def test_convert_corners(grid, dataset, tile_corners, src, dest, result):
    """Validate a tile's x,y corners converted to different units."""
    assert tiles.convert_corners(grid, dataset, tile_corners, src, dest) == result


##-- Tile Transformations --##
@pytest.mark.parametrize(
    "tg_info, h_v, result",
    [
        (
            {
                "rx": 1,
                "ry": -1,
                "tx": 2565585,
                "ty": 3314805,
                "sx": 150000,
                "sy": 150000,
            },
            {"h": 31, "v": 6},
            {"x": 2084415.0, "y": 2414805.0},
        ),
    ],
)
def test_tile_to_projection(tg_info, h_v, result):
    """Validate conversion of tile id to x,y coordinates."""
    assert tiles.to_projection(tg_info, h_v) == result


@pytest.mark.parametrize(
    "h_v, result", [({"h": 31, "v": 6}, [31, 6]),],
)
def test_point_matrix(h_v, result):
    """Validate transformation of tile hv to a matrix."""
    assert tiles.point_matrix(h_v)[0] == result[0]
    assert tiles.point_matrix(h_v)[1] == result[1]


@pytest.mark.parametrize(
    "tile_grid_info, result",
    [
        (
            {
                "rx": 1,
                "ry": -1,
                "tx": 2565585,
                "ty": 3314805,
                "sx": 150000,
                "sy": 150000,
            },
            [6.666666666666667e-06],
        ),
    ],
)
def test_transform_matrix(tile_grid_info, result):
    """Validate the transformation dictionary creation."""
    assert tiles.transform_matrix(tile_grid_info)[0][0] == result[0]


@pytest.mark.parametrize(
    "tile_id, result", [("031006", {"h": 31, "v": 6}),],
)
def test_string_to_tile(tile_id, result):
    """Validate conversion of a tile id string to a hv dictionary."""
    assert tiles.string_to_tile(tile_id) == result


@pytest.mark.parametrize(
    "h_v, result", [({"h": 31, "v": 6}, "031006"), ({"h": 123, "v": 456}, "123456"),],
)
def test_tile_to_string(h_v, result):
    """Validate tile h_v to tile id string conversion."""
    assert tiles.tile_to_string(h_v) == result


@pytest.mark.parametrize(
    "grid, dataset, result", [("cu", "ard", {"x_int": 150000.0, "y_int": -150000.0}),],
)
def test_tile_interval(grid, dataset, result):
    """Validate retrieval of tile intervals."""
    assert tiles.interval(grid, dataset) == result
