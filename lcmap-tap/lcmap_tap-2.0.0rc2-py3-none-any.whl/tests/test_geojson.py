"""
Unit tests for lcmap_tap/MapCanvas/geojson.py
"""
from contextlib import ExitStack as does_not_raise
import os
import pytest
from lcmap_tap.MapCanvas import geojson


@pytest.mark.parametrize(
    "grid, dataset, result", [("cu", "ard", True),],
)
def test_write_tile_overlay(grid, dataset, result):
    """Validate tile overlay file gen/write."""
    geojson.write_tile_overlay(grid, dataset)
    out_file = os.path.join(geojson.js_overlay_path(), geojson.js_overlay_file(grid))
    assert os.path.isfile(out_file) == result


@pytest.mark.parametrize(
    "result", [("/geojson.py"),],
)
def test_js_overlay_path(result):
    """Validate returned path."""
    assert os.path.isfile(geojson.js_overlay_path() + result)


@pytest.mark.parametrize(
    "grid, result", [("cu", "hv-tiles-cu.js"),],
)
def test_js_overlay_file(grid, result):
    """Validate returned filename."""
    assert geojson.js_overlay_file(grid) == result


@pytest.mark.parametrize(
    "grid, dataset, result",
    [
        (
            "cu",
            "ard",
            {
                "hv": "h32v3",
                "tile_ul": "-66.88687358195142, 45.66670475157042",
                "tile_ll": "-67.45610994454883, 44.38016421334179",
            },
        ),
    ],
)
def test_hv_tiles(grid, dataset, result):
    """Validate Javascript variable for GeoJSON generated features."""
    js_hv_tiles = geojson.hv_tiles(grid, dataset)
    print(f"js_hv_tiles: {js_hv_tiles[:1520]}")
    assert result["hv"] in js_hv_tiles
    assert result["tile_ul"] in js_hv_tiles
    assert result["tile_ll"] in js_hv_tiles


@pytest.mark.parametrize(
    "match, result",
    [
        ("var hv_tiles", does_not_raise()),
        ("FeatureCollection", does_not_raise()),
        ("features", does_not_raise()),
        ("coordinates", pytest.raises(AssertionError)),
    ],
)
def test_header(match, result):
    """Validate the GeoJSON header string."""
    with result:
        assert match in geojson.header()


@pytest.mark.parametrize(
    "match, result",
    [("]}];", does_not_raise()), ("coordinates", pytest.raises(AssertionError)),],
)
def test_footer(match, result):
    """Validate the GeoJSON footer string."""
    with result:
        assert match in geojson.footer()


@pytest.mark.parametrize(
    "match, result",
    [
        ("tile_h", does_not_raise()),
        ("tile_v", does_not_raise()),
        ("ll_long", does_not_raise()),
        ("ll_lat", does_not_raise()),
        ("lr_long", does_not_raise()),
        ("lr_lat", does_not_raise()),
        ("ur_long", does_not_raise()),
        ("ur_lat", does_not_raise()),
        ("ul_long", does_not_raise()),
        ("ul_lat", does_not_raise()),
        ("var hv_tiles", pytest.raises(AssertionError)),
    ],
)
def test_feature_template(match, result):
    """Validate the GeoJSON feature template string."""
    with result:
        assert match in geojson.feature_template()


@pytest.mark.parametrize(
    "fid, tile_info, result",
    [
        (
            0,
            (
                {"h": 32, "v": 3},
                {
                    "tile_ul": {"x": -66.88689165841076, "y": 45.66669610027017},
                    "tile_ur": {"x": -65.06384006055114, "y": 45.247380054150184},
                    "tile_lr": {"x": -65.66385925124207, "y": 43.969936870803494},
                    "tile_ll": {"x": -67.45612734227188, "y": 44.38015611585466},
                },
            ),
            {
                "fid": 0,
                "tile_h": 32,
                "tile_v": 3,
                "ll_long": -67.45612734227188,
                "ll_lat": 44.38015611585466,
                "lr_long": -65.66385925124207,
                "lr_lat": 43.969936870803494,
                "ur_long": -65.06384006055114,
                "ur_lat": 45.247380054150184,
                "ul_long": -66.88689165841076,
                "ul_lat": 45.66669610027017,
            },
        ),
    ],
)
def test_template_vars(fid, tile_info, result):
    """Validate the template var diciontary data structure."""
    assert geojson.template_vars(fid, tile_info) == result
