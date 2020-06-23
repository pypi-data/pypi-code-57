"""
Unit tests for lcmap_tap/storage/local.py
"""
from contextlib import ExitStack as does_not_raise
import os
from collections import namedtuple
import pytest
import lcmap_tap
from lcmap_tap.storage import local

GeoCoordinate = namedtuple("GeoCoordinate", ["x", "y"])

chips = [(-408585, 2327805), (123456, 789012)]
pixels = [(-408585, 2324835), (123456, 789012)]
x = 0
y = 1

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


##-- Config File Functions --##
@pytest.mark.parametrize(
    "config, result",
    [
        (
            os.path.join(lcmap_tap.top_dir(), "config-example.yaml"),
            does_not_raise(),
        ),
        (
            os.path.join(lcmap_tap.top_dir(), "not-a-config-file"),
            pytest.raises(TypeError),
        ),
    ],
)
def test_load_config(config, result):
    """
    Verify loading yaml config files works
    """
    with result:
        assert local.load_config(config)["ARD_BASE_URL"] is not None


##-- Cache File Saving/Writing to Disk --##
@pytest.mark.parametrize(
    "cache_type, cache_data, chip_coord_ul, result",
    [
        (
            "prediction",
            prediction_test_data,
            GeoCoordinate(chips[0][x], chips[0][y]),
            does_not_raise(),
        ),
    ],
)
def test_save_cache(cache_type, cache_data, chip_coord_ul, result):
    """
    Test saving an object to cache.
    """
    with result:
        local.save_cache(
            cache_type=cache_type, cache_data=cache_data, chip_coord_ul=chip_coord_ul
        )


@pytest.mark.parametrize(
    "cache_data, file_name, result",
    [(prediction_test_data, "/tmp/test_safe_to_delete_me.json", does_not_raise()),],
)
def test_save_cache_file(cache_data, file_name, result):
    """
    Test saving an object to disk.
    """
    with result:
        local.save_cache_file(cache_data=cache_data, file_name=file_name)


@pytest.mark.parametrize(
    "cache_data, file_name, result",
    [(prediction_test_data, "/tmp/test_safe_to_delete_me.json", does_not_raise()),],
)
def test_save_json(cache_data, file_name, result):
    """
    Test saving a json object to disk.
    """
    with result:
        local.save_json(cache_data=cache_data, file_name=file_name)


##-- Cache File Loading/Reading from Disk --##
@pytest.mark.parametrize(
    "cache_type, chip_coord_ul, result",
    [("prediction", GeoCoordinate(chips[0][x], chips[0][y]), True,),],
)
def test_read_cache(cache_type, chip_coord_ul, result):
    """
    Test reading a file from the cache.
    This test file should have been written to local disk by the
    'test_save_cache' unit test.
    """
    loaded_file = local.read_cache(cache_type=cache_type, chip_coord_ul=chip_coord_ul)
    print(f"-> Loaded file is: {loaded_file}")
    assert bool(loaded_file) == result


@pytest.mark.parametrize(
    "file_name, result",
    [("tests/does_not_exist.json", False), ("tests/884415-914805.json", True),],
)
def test_load_cache_file(file_name, result):
    """
    Test loading a file from disk.
    """
    loaded_file = local.load_cache_file(file_name=file_name)
    print(f"-> Loaded file is: {loaded_file}")
    assert bool(loaded_file) == result


@pytest.mark.parametrize(
    "file_name, result",
    [
        ("tests/does_not_exist.json", pytest.raises(FileNotFoundError)),
        ("tests/884415-914805.json", does_not_raise()),
    ],
)
def test_load_json(file_name, result):
    """
    Test loading a json file handle.
    """
    with result, open(file_name) as f:
        assert local.load_json(file_name=f) is not None


##-- Cache File Name Generation --##
@pytest.mark.parametrize(
    "file_type, chip_coord_ul, result",
    [
        (
            "ard",
            GeoCoordinate(chips[0][x], chips[0][y]),
            "/ard_cache/-408585-2327805.p",
        ),
        (
            "pixel",
            GeoCoordinate(chips[0][x], chips[0][y]),
            "/pixel_cache/-408585-2327805.json",
        ),
        (
            "prediction",
            GeoCoordinate(chips[0][x], chips[0][y]),
            "/prediction_cache/-408585-2327805.json",
        ),
        (
            "segment",
            GeoCoordinate(chips[0][x], chips[0][y]),
            "/segment_cache/-408585-2327805.json",
        ),
    ],
)
def test_cache_file_path(file_type, chip_coord_ul, result):
    """
    Test full path to file generation.
    """
    generated_full_path = local.cache_file_path(
        file_type=file_type, chip_coord_ul=chip_coord_ul
    )
    print(f"-> generated_full_path is: {generated_full_path}")
    assert generated_full_path.endswith(result)


@pytest.mark.parametrize(
    "file_type, result",
    [
        ("ard", "/ard_cache"),
        ("pixel", "/pixel_cache"),
        ("prediction", "/prediction_cache"),
        ("segment", "/segment_cache"),
    ],
)
def test_cache_dir_name(file_type, result):
    """
    Test directory path name generation.
    """
    generated_path = local.cache_dir_name(file_type=file_type)
    print(f"-> generated_path is: {generated_path}")
    assert generated_path.endswith(result)


@pytest.mark.parametrize(
    "file_type, chip_coord_ul, result",
    [
        ("ard", GeoCoordinate(chips[0][x], chips[0][y]), "-408585-2327805.p"),
        ("pixel", GeoCoordinate(chips[0][x], chips[0][y]), "-408585-2327805.json"),
        ("prediction", GeoCoordinate(chips[0][x], chips[0][y]), "-408585-2327805.json"),
        ("segment", GeoCoordinate(chips[0][x], chips[0][y]), "-408585-2327805.json"),
    ],
)
def test_cache_file_name(file_type, chip_coord_ul, result):
    """
    Test cache filename generation.
    """
    generated_name = local.cache_file_name(
        file_type=file_type, chip_coord_ul=chip_coord_ul
    )
    print(f"-> generated_name is: {generated_name}")
    assert generated_name == result
